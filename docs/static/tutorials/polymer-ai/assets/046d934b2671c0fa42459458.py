"""L17: scattering measurements, inverse prediction, and calibrated intervals.
Install: numpy scipy scikit-learn torch matplotlib requests
Run: python example.py
Experimental source: SASBDB SASDPT4; synthetic ellipsoids supply known targets.
"""
from pathlib import Path
import json,copy
import numpy as np
from numpy.polynomial.legendre import leggauss
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
import torch
from torch import nn
torch.set_num_threads(2)
HERE=Path.cwd()
OUT=HERE/"scattering_outputs";OUT.mkdir(exist_ok=True)
rng=np.random.default_rng(1717);q=np.linspace(.05,1.2,96)
rg=rng.uniform(1.2,3.2,480);aspect=np.exp(rng.uniform(np.log(.5),np.log(2.5),480))
axes_a=rg*np.sqrt(5/(2+aspect**2));axes_c=axes_a*aspect
def formfactor(q,a,c,n=80):
    x,w=leggauss(n);u=(x+1)/2;w=w/2
    R=np.sqrt(a[:,None]**2*(1-u*u)+c[:,None]**2*u*u)
    z=q[None,:,None]*R[:,None,:]
    amp=np.where(abs(z)<1e-3,1-z*z/10+z**4/280,3*(np.sin(z)-z*np.cos(z))/np.where(z==0,1,z)**3)
    return np.sum(amp*amp*w,axis=2)
P=formfactor(q,axes_a,axes_c)
assert abs(formfactor(np.array([0.]),axes_a,axes_c)-1).max()<1e-14
amplitude=rng.uniform(.8,1.2,(480,2));exposure=rng.uniform(20000,80000,(480,2))
buffer=.08+.02*q*q
def observe(exposure):
    sample=rng.poisson(exposure[:,:,None]*(amplitude[:,:,None]*P[:,None,:]+buffer))
    blank=rng.poisson(exposure[:,:,None]*buffer)
    return (sample-blank)/exposure[:,:,None],np.sqrt(sample+blank)/exposure[:,:,None],sample,blank
y,sd,sample_counts,blank_counts=observe(exposure)
order=rng.permutation(480);groups=dict(train=order[:240],validation=order[240:320],calibration=order[320:400],test=order[400:])
rows={k:np.array([2*i+j for i in v for j in range(2)]) for k,v in groups.items()}
Y=np.repeat(rg,2);raw=y.reshape(-1,96);uncertainty=sd.reshape(-1,96)
def features(v):return v/v[:,:4].mean(1,keepdims=True)
scaler=StandardScaler().fit(features(raw)[rows['train']]);X=scaler.transform(features(raw))
target_mean=Y[rows['train']].mean();target_sd=Y[rows['train']].std()
ridge=Ridge(alpha=1.).fit(X[rows['train']],Y[rows['train']])
def guinier(v,s,available=None):
    if available is None:available=np.ones(96,dtype=bool)
    preds=[];ses=[]
    for yy,ss in zip(v,s):
        mask=(q>=.05)&(q<=.3)&available&(yy>0)&(ss>0)
        A=np.column_stack([np.ones(mask.sum()),q[mask]**2]);err=ss[mask]/yy[mask]
        Aw=A/err[:,None];cov=np.linalg.inv(Aw.T@Aw);coef=cov@(Aw.T@(np.log(yy[mask])/err))
        value=np.sqrt(-3*coef[1]) if coef[1]<0 else np.nan
        preds.append(value);ses.append(3*np.sqrt(cov[1,1])/(2*value))
    return np.array(preds),np.array(ses)
physics,physics_se=guinier(raw,uncertainty)
class Network(nn.Module):
    def __init__(self):
        super().__init__();self.layers=nn.Sequential(nn.Linear(96,64),nn.Tanh(),nn.Linear(64,32),nn.Tanh(),nn.Linear(32,1))
    def forward(self,x):return self.layers(x).squeeze(-1)
xt=torch.tensor(X,dtype=torch.float32);yt=torch.tensor((Y-target_mean)/target_sd,dtype=torch.float32)
models=[];curves=[];seed_preds=[]
for seed in [17,27,37]:
    torch.manual_seed(seed);model=Network();optimizer=torch.optim.Adam(model.parameters(),lr=.003)
    best=float('inf');best_state=None;curve=[];best_epoch=0
    for epoch in range(1,301):
        model.train();optimizer.zero_grad();pred=model(xt[rows['train']]);loss=((pred-yt[rows['train']])**2).mean();loss.backward();optimizer.step()
        if epoch%5==0:
            model.eval()
            with torch.no_grad():v=float(((model(xt[rows['validation']])-yt[rows['validation']])**2).mean())
            curve.append([epoch,float(loss.detach()),v])
            if v<best:best=v;best_state=copy.deepcopy(model.state_dict());best_epoch=epoch
    model.load_state_dict(best_state);model.eval()
    with torch.no_grad():seed_preds.append(model(xt).numpy()*target_sd+target_mean)
    models.append(dict(seed=seed,epoch=best_epoch,validation_mse_scaled=best,parameters=sum(p.numel() for p in model.parameters()),weights={k:v.tolist() for k,v in best_state.items()}))
    curves.append(curve);print('seed',seed,'epoch',best_epoch,'validationRMSEnm',best**.5*target_sd,flush=True)
nominal=dict(mean=np.full(960,target_mean),guinier=physics,ridge=ridge.predict(X),mlp=np.mean(seed_preds,axis=0))
def mlp_predict(features):
    x=torch.tensor(features,dtype=torch.float32);out=[]
    for item in models:
        model=Network();model.load_state_dict({k:torch.tensor(v) for k,v in item['weights'].items()});model.eval()
        with torch.no_grad():out.append(model(x).numpy()*target_sd+target_mean)
    return np.mean(out,axis=0)
test=rows['test'];gtest=groups['test'];variants={}
noisy,noisy_sd,_,_=observe(exposure/9)
variant_raw={'nominal':raw[test],'noise3x':noisy.reshape(-1,96)[test],
    'background':raw[test]+.04*amplitude.reshape(-1)[test,None]}
variant_sd={'nominal':uncertainty[test],'noise3x':noisy_sd.reshape(-1,96)[test],'background':uncertainty[test]}
cropped=raw[test].copy();first=int(np.flatnonzero(q>=.25)[0]);cropped[:,:first]=cropped[:,first,None]
variant_raw['missing_lowq']=cropped;variant_sd['missing_lowq']=uncertainty[test]
for variant,v in variant_raw.items():
    x=scaler.transform(features(v));available=q>=.25 if variant=='missing_lowq' else None
    phys,se=guinier(v,variant_sd[variant],available)
    variants[variant]=dict(mean=np.full(len(test),target_mean),guinier=phys,ridge=ridge.predict(x),mlp=mlp_predict(x))
widths={};scores={};coverage={}
for name,pred in nominal.items():
    calerr=abs(pred[rows['calibration']]-Y[rows['calibration']]).reshape(-1,2).max(1)
    widths[name]=float(np.sort(calerr)[72]);scores[name]={};coverage[name]={}
    for variant,preds in variants.items():
        p=preds[name];valid=np.isfinite(p);err=abs(p-Y[test]).reshape(-1,2)
        scores[name][variant]=dict(RMSE_nm=float(np.sqrt(np.mean((p[valid]-Y[test][valid])**2))),
            MAE_nm=float(np.mean(abs(p[valid]-Y[test][valid]))),valid_predictions=int(valid.sum()),total=len(p))
        coverage[name][variant]=dict(simultaneous_object_coverage=float(np.mean(np.all(err<=widths[name],axis=1))),
            marginal_record_coverage=float(np.mean(err<=widths[name])),interval_width_nm=2*widths[name])
result=dict(seed=1717,groups={k:v.tolist() for k,v in groups.items()},rows={k:v.tolist() for k,v in rows.items()},
    q_nm_inverse=q.tolist(),geometry=dict(Rg_nm=rg.tolist(),aspect=aspect.tolist(),a_nm=axes_a.tolist(),c_nm=axes_c.tolist()),
    input_scaler=dict(mean=scaler.mean_.tolist(),scale=scaler.scale_.tolist()),target_scaler=dict(mean=target_mean,scale=target_sd),
    ridge=dict(coef=ridge.coef_.tolist(),intercept=float(ridge.intercept_)),models=models,training_curves=curves,
    conformal_halfwidth_nm=widths,scores=scores,coverage=coverage)

np.savez_compressed(OUT/'predictions.npz',q=q,Rg=Y,y=raw,sigma=uncertainty,formfactor=P,amplitude=amplitude,exposure=exposure,
    sample_counts=sample_counts,blank_counts=blank_counts,guinier_se=physics_se,**{'full_'+k:v for k,v in nominal.items()},
    **{variant+'_'+name:p for variant,preds in variants.items() for name,p in preds.items()},
    **{variant+'_raw':v for variant,v in variant_raw.items()},**{variant+'_sigma':v for variant,v in variant_sd.items()})


# The experimental file is a processed consensus profile; q is originally A^-1.
import hashlib,requests
SOURCE='https://www.sasbdb.org/media/intensities_files/SASDPT4.dat'
SOURCE_SHA='391686994c1c9ba5e85514962addbd169298cb6c4a288c644c370641ca3dfedb'
path=HERE/'SASDPT4.dat'
if not path.exists():
    response=requests.get(SOURCE,timeout=(15,45));response.raise_for_status();path.write_bytes(response.content)
assert hashlib.sha256(path.read_bytes()).hexdigest()==SOURCE_SHA
data=[]
for line in path.read_text().splitlines():
    parts=line.split()
    if len(parts)==3:
        try:data.append(list(map(float,parts)))
        except ValueError:pass
data=np.array(data);assert data.shape==(200,3) and np.all(data[:,1:]>0)
qe=data[:,0]*10;Ie=data[:,1];se=data[:,2]
def experimental_fit(qmax):
    mask=(qe>=.1)&(qe<=qmax+1e-12);A=np.column_stack([np.ones(mask.sum()),qe[mask]**2])
    logI=np.log(Ie[mask]);error=se[mask]/Ie[mask];Aw=A/error[:,None]
    cov=np.linalg.inv(Aw.T@Aw);coef=cov@(Aw.T@(logI/error))
    R=np.sqrt(-3*coef[1]);residual=(logI-A@coef)/error
    return dict(qmin=.1,qmax=qmax,n=int(mask.sum()),Rg_nm=float(R),I0=float(np.exp(coef[0])),
        conditional_Rg_se_nm=float(3*np.sqrt(cov[1,1])/(2*R)),
        reduced_chi2=float(residual@residual/(mask.sum()-2)),qmaxRg=float(qmax*R),
        intercept=float(coef[0]),slope_nm2=float(coef[1]),residual=residual.tolist())
fits=[experimental_fit(qmax) for qmax in [.4,.5,.6,.7,.8,.85,.9]];fit=fits[4]
result['experiment']=dict(entry='SASDPT4',doi='10.1107/S2059798322009184',source_url=SOURCE,sha256=SOURCE_SHA,
    rows=200,original_q_unit='angstrom^-1',analysis_q_unit='nm^-1',conversion=10,
    intensity='relative consensus intensity; solvent already subtracted',main_fit=fit,window_sensitivity=fits,
    uncertainty='Conditional WLS covariance using propagated point errors; residual and window sensitivity reported separately')
result['data_definition']=dict(objects=480,repeats=2,train_objects=240,validation_objects=80,calibration_objects=80,test_objects=80,
    calibration='73rd of80 objectmaxscores; twoobservations treated as one exchangeableobject',
    perturbations='Pairedheldoutobjects; N/9counts, +0.04*I0residualbackground, missingq<0.25nm^-1',
    missing_policy='Constant prefixfill forfixedgridlearners; excludeunobservedpointsfromGuinier; 1invalidGuinierslope retainedasNaN inNPZ and counteduncovered')
(OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
samples=dict(object_id=np.repeat(np.arange(480),2).tolist(),repeat=np.tile([0,1],480).tolist(),groups=result['groups'],
    q_nm_inverse=q.tolist(),Rg_true_nm=Y.tolist(),observed_intensity=raw.tolist(),standard_error=uncertainty.tolist(),
    amplitude=amplitude.tolist(),exposure=exposure.tolist(),sample_counts=sample_counts.tolist(),blank_counts=blank_counts.tolist())
(OUT/'samples.json').write_text(json.dumps(samples,separators=(',',':'))+'\n',encoding='utf-8')
(OUT/'experimental.json').write_text(json.dumps(dict(q_nm_inverse=qe.tolist(),intensity=Ie.tolist(),standard_error=se.tolist()),indent=2)+'\n',encoding='utf-8')

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,
    'axes.labelcolor':'#30453f','text.color':'#243d35','axes.edgecolor':'#bac7c0','xtick.color':'#53675e',
    'ytick.color':'#53675e','svg.hashsalt':'L17-scattering','figure.facecolor':'#fffef9','axes.facecolor':'#fffef9'})
names=['mean','guinier','ridge','mlp'];labels=['Training mean','Guinier fit','Ridge curve map','MLP curve map']
colors=['#a69b86','#b78150','#367e9d','#287b63']
def style(ax,title,xlabel,ylabel):
    ax.set_title(title,loc='left',fontsize=12,pad=13,weight='bold');ax.set_xlabel(xlabel);ax.set_ylabel(ylabel)
    ax.grid(axis='y',alpha=.18);ax.set_axisbelow(True)
def panel(i,fig,spec):
    if i==1:
        grid=spec.subgridspec(2,1,height_ratios=[2,1],hspace=.08)
        ax=fig.add_subplot(grid[0]);res=fig.add_subplot(grid[1]);mask=(qe>=.1)&(qe<=.8+1e-12)
        show=qe<=1.2;outside=show&~mask
        ax.errorbar(qe[mask]**2,np.log(Ie[mask]),yerr=se[mask]/Ie[mask],fmt='o',ms=4,color='#287b63',capsize=2,label='Fitted window')
        ax.scatter(qe[outside]**2,np.log(Ie[outside]),facecolor='white',edgecolor='#a0b3a6',s=22,label='Displayed, not fitted')
        gridq=np.linspace(0,1.2,180);ax.plot(gridq**2,fit['intercept']+fit['slope_nm2']*gridq**2,color='#b78150',lw=1.5)
        style(ax,'B  Low-angle fit and residuals','','ln I(q)');ax.legend(frameon=False,fontsize=8,loc='upper right')
        ax.text(.03,.05,f"Rg = {fit['Rg_nm']:.4f} nm\nConditional SE = {fit['conditional_Rg_se_nm']:.4f} nm",transform=ax.transAxes,fontsize=9)
        res.axhline(0,color='#a7b9ad',lw=1);res.axhspan(-2,2,color='#e9eee4');res.plot(qe[mask]**2,fit['residual'],'o-',ms=4,color='#287b63')
        style(res,'','q² (nm⁻²)','Residual / SE');ax.tick_params(labelbottom=False)
        ax.set_xlim(0,1.5);res.set_xlim(0,1.5)
        return
    ax=fig.add_subplot(spec)
    if i==0:
        ax.errorbar(qe,Ie,yerr=se,fmt='.',ms=3,color='#287b63',ecolor='#9db9a9',lw=.7)
        ax.axvspan(.1,.8,color='#ede5d4',alpha=.65,zorder=0);ax.set_xscale('log');ax.set_yscale('log')
        style(ax,'A  Lysozyme consensus: measured profile','q (nm⁻¹, log scale)','Relative intensity (log scale)')
        ax.text(.97,.94,'SASDPT4\n200 observed points\nShading: Guinier fit window',transform=ax.transAxes,ha='right',va='top',fontsize=9)
    elif i==2:
        k=int(test[0]);obj=k//2;rep=k%2;N=exposure[obj,rep]
        ax.plot(q,sample_counts[obj,rep]/N,color='#788b99',lw=1.1,label='Sample + buffer counts / N')
        ax.plot(q,blank_counts[obj,rep]/N,color='#b78150',lw=1.1,label='Buffer counts / N')
        ax.errorbar(q,raw[k],yerr=uncertainty[k],fmt='.',ms=3,elinewidth=.5,color='#287b63',label='Subtracted observation')
        ax.plot(q,amplitude[obj,rep]*P[obj],color='#223c35',ls='--',lw=1.5,label='Known synthetic signal')
        style(ax,'C  A controlled measurement','q (nm⁻¹)','Relative intensity');ax.legend(frameon=False,fontsize=8,loc='upper right')
        ax.text(.03,.19,f'Object {obj}, repeat {rep+1}\nRg = {Y[k]:.3f} nm',transform=ax.transAxes,fontsize=9)
    elif i==3:
        ax.plot([1.1,3.3],[1.1,3.3],color='#a3b5a8',lw=1.2)
        for name,label,color in zip(names[1:],labels[1:],colors[1:]):
            ax.scatter(Y[test],variants['nominal'][name],s=19,color=color,alpha=.55,label=label)
        style(ax,'D  Held-out sizes from curves','True synthetic Rg (nm)','Predicted Rg (nm)');ax.set(xlim=(1.1,3.3),ylim=(1.1,3.3))
        ax.legend(frameon=False,fontsize=9,loc='upper left');ax.text(.97,.04,'80 objects × 2 observations',transform=ax.transAxes,ha='right',fontsize=9)
    elif i==4:
        xx=np.arange(4);families=['nominal','noise3x','background','missing_lowq']
        for j,(name,label,color) in enumerate(zip(names,labels,colors)):
            values=[scores[name][s]['RMSE_nm'] for s in families]
            ax.bar(xx+(j-1.5)*.18,values,.16,color=color,label=label)
        ax.set_xticks(xx,['Nominal','Noise ×3','Background','Missing low q']);ax.set_yscale('log');ax.set_ylim(.01,1.5)
        style(ax,'E  Change the measurement conditions','','Rg RMSE (nm, log scale)')
        ax.legend(frameon=False,fontsize=8,ncol=2,loc='upper left')
        ax.text(.02,.03,'Missing q: Guinier 159 valid / 160 total',transform=ax.transAxes,fontsize=8,bbox=dict(facecolor='#fffef9',edgecolor='none',alpha=.9,pad=3))
    else:
        xx=np.arange(4);families=['nominal','noise3x','background','missing_lowq']
        ax.axhline(.9,color='#a7b6aa',ls='--',lw=1.2)
        for name,label,color in zip(names[1:],labels[1:],colors[1:]):
            values=[coverage[name][s]['simultaneous_object_coverage'] for s in families]
            ax.plot(xx,values,'o-',lw=1.5,ms=5,color=color,label=f'{label}: width {2*widths[name]:.3f} nm')
        ax.set_xticks(xx,['Nominal','Noise ×3','Background','Missing low q']);ax.set_ylim(-.04,1.2)
        style(ax,'F  Keep the calibrated intervals fixed','','Both repeats covered / object')
        ax.legend(frameon=False,fontsize=8,loc='upper right');ax.text(.02,.04,'90% target · 80 calibration objects\nPaired shifts use the same 80 test objects',transform=ax.transAxes,fontsize=8)
keys=['real_curve','guinier','measurement','prediction','shifts','coverage']
for i,key in enumerate(keys):
    fig=plt.figure(figsize=(8.2,5.1),layout='constrained');panel(i,fig,fig.add_gridspec(1,1)[0])
    fig.savefig(OUT/f'{key}.svg',metadata={'Date':None});plt.close(fig)
fig=plt.figure(figsize=(16.4,15.3),layout='constrained');grid=fig.add_gridspec(3,2,hspace=.09,wspace=.05)
for i in range(6):panel(i,fig,grid[i//2,i%2])
fig.savefig(OUT/'scattering_learning.svg',metadata={'Date':None})
fig.savefig(OUT/'scattering_learning.png',dpi=160,metadata={'Software':'L17 reproducible example'});plt.close(fig)
print(f"SASDPT4: 200 measured points; original q in A^-1 converted to nm^-1")
print(f"Fixed experimental window0.1–0.8nm^-1: Rg {fit['Rg_nm']:.6f}nm; conditional SE {fit['conditional_Rg_se_nm']:.6f}nm; reduced chi2 {fit['reduced_chi2']:.3f}")
print('Synthetic objects: 240train / 80validation / 80calibration / 80test; 2observations each')
for name,label in zip(names,labels):
    print(f"{label:20s}: nominal RMSE {scores[name]['nominal']['RMSE_nm']:.6f}nm; joint coverage {coverage[name]['nominal']['simultaneous_object_coverage']:.3f}")
print('Missing low q: 1of160Guinier slopes is positive; invalidestimate retained andcountedasuncovered')
print('Six figures, full generated observations and model weights: scattering_outputs/')
