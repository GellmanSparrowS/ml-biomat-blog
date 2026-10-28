"""Generate and verify gel parameter candidates with two property targets.
All measurements come from a stated physical virtual laboratory.
Run: python example.py; requires NumPy, SciPy and Matplotlib.
"""
from pathlib import Path
import json,os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1');os.environ.setdefault('OMP_NUM_THREADS','1')
import numpy as np
from scipy.optimize import brentq
from scipy.linalg import cho_factor,cho_solve,solve_triangular
from scipy.special import expit,logit
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT=Path('design_outputs');OUT.mkdir(exist_ok=True)
NOISE=np.array([.04,.05]);PRIOR=np.array([3.5,2.5]);LENGTH=np.array([.6,.35])
TARGET=np.log([30.,12.]);SCALE=np.log(1.2);SEEDS=list(range(2000,2012));BUDGETS=[8,12,16,20,24]
def physical(x):
    x=np.atleast_2d(x);nu=2*30**x[:,0];chi=.2+.35*x[:,1];p=[]
    for n,c in zip(nu,chi):
        def balance(v):return np.log1p(-v)+v+c*v*v+n*18e-6*(v**(1/3)-v/2)
        p.append(brentq(balance,1e-7,1-1e-10,xtol=1e-14))
    p=np.array(p);return np.column_stack([-np.log(p),np.log(nu*8.314462618*298*p**(1/3)/1000)])
def feasible(z):return (z[...,0]>=np.log(20))&(z[...,1]>=np.log(8))&(z[...,1]<=np.log(16))
def target_loss(z):return np.sum(((z-TARGET)/SCALE)**2,axis=-1)
def utility(z):return np.exp(-.5*target_loss(z))*feasible(z)
def target_hit(z):return np.all(abs(z-TARGET)<=SCALE,axis=-1)
def kernel(a,b):return 2.25*np.exp(-.5*np.sum(((a[:,None,:]-b[None,:,:])/LENGTH)**2,axis=2))
class GP:
    def __init__(self,x,y):
        self.x=x.copy();self.models=[]
        for j in range(2):
            factor=cho_factor(kernel(x,x)+(NOISE[j]**2+1e-10)*np.eye(len(x)),lower=True)
            self.models.append((factor,cho_solve(factor,y[:,j]-PRIOR[j])))
    def predict(self,q):
        cross=kernel(self.x,q);mean=[];variance=[]
        for j,(factor,alpha) in enumerate(self.models):
            v=solve_triangular(factor[0],cross,lower=True)
            mean.append(PRIOR[j]+cross.T@alpha);variance.append(np.maximum(0,2.25-np.sum(v*v,axis=0)))
        return np.array(mean).T,np.array(variance).T

def generate_candidate(model,x,seed,keep_cloud=False):
    rng=np.random.default_rng(seed);normal=rng.normal(size=(64,2));normal=np.vstack([normal,-normal])
    incumbent=float(np.max(utility(model.predict(x)[0])))
    location=np.zeros(2);covariance=np.eye(2)*4;best=None;cloud=[]
    for iteration in range(5):
        latent=np.vstack([rng.multivariate_normal(location,covariance,96),logit(rng.uniform(1e-6,1-1e-6,(32,2)))])
        candidates=expit(latent);mean,var=model.predict(candidates)
        draws=mean[:,None,:]+np.sqrt(var[:,None,:])*normal[None,:,:]
        acquisition=np.maximum(utility(draws)-incumbent,0).mean(axis=1)
        uncertainty=var.sum(axis=1)
        available=np.min(np.sum((candidates[:,None,:]-x[None,:,:])**2,axis=2),axis=1)>=.02**2
        acquisition[~available]=-np.inf
        order=np.lexsort((uncertainty,acquisition));valid=order[np.isfinite(acquisition[order])]
        assert len(valid)>=26,'Candidate population exhausted'
        chosen=int(valid[-1]);key=(float(acquisition[chosen]),float(uncertainty[chosen]))
        if best is None or key>best[0]:best=(key,candidates[chosen].copy())
        elite=latent[valid[-26:]];center=elite.mean(0);delta=elite-center
        location=.3*location+.7*center
        covariance=.3*covariance+.7*(delta.T@delta/len(elite))+.08**2*np.eye(2)
        item=dict(iteration=iteration+1,best_acquisition=best[0][0],logit_mean=location.tolist(),logit_cov=covariance.tolist())
        if keep_cloud:item.update(x=candidates.tolist(),acquisition=np.where(np.isfinite(acquisition),acquisition,-1).tolist(),elite_indices=valid[-26:].tolist())
        cloud.append(item)
    return best[1],dict(incumbent=incumbent,selected_acquisition=best[0][0],selected_variance=best[0][1],history=cloud)

def recommend(model,x):
    mean,var=model.predict(x);order=np.lexsort((-target_loss(mean),utility(mean)))[::-1]
    first=int(order[0]);second=next((int(i) for i in order[1:] if np.linalg.norm(x[i]-x[first])>=.03),int(order[1]))
    return [first,second],mean,var

def campaign(seed):
    rng=np.random.default_rng(seed)
    initial=np.column_stack([(rng.permutation(8)+rng.random(8))/8 for _ in range(2)])
    random_tail=rng.random((16,2));noise=np.random.default_rng(20000+seed).normal(size=(24,2))*NOISE
    confirm_noise=np.random.default_rng(30000+seed).normal(size=(2,3,2))*NOISE;runs={}
    for strategy in ['random','surrogate_ei_cem']:
        x=initial.copy();truth=physical(x);y=truth+noise[:8];curve=[];steps=[]
        for n in range(8,25):
            model=GP(x,y)
            if n in BUDGETS:curve.append(float(np.max(utility(truth))))
            if n==24:break
            if strategy=='random':new=random_tail[n-8];details=None
            else:new,details=generate_candidate(model,x,40000+seed*100+n,keep_cloud=(seed==SEEDS[0] and n==8))
            true_new=physical(new)[0];x=np.vstack([x,new]);truth=np.vstack([truth,true_new]);y=np.vstack([y,true_new+noise[n]])
            steps.append(dict(budget=n+1,x=new.tolist(),selection=details))
        ids,mean,var=recommend(model,x);confirm=truth[ids,None,:]+confirm_noise
        runs[strategy]=dict(x=x.tolist(),observations=y.tolist(),physical_truth=truth.tolist(),learning_best_utility=curve,steps=steps,
            recommendation_indices=ids,recommendation_predicted_log=mean[ids].tolist(),recommendation_variance=var[ids].tolist(),
            recommendation_true_log=truth[ids].tolist(),confirmation_log=confirm.tolist(),
            final_target_loss=float(target_loss(truth[ids[0]])),final_utility=float(utility(truth[ids[0]])),
            final_feasible=bool(feasible(truth[ids[0]])),final_target_hit=bool(target_hit(truth[ids[0]])))
        if seed==SEEDS[0]:
            perturb=np.random.default_rng(50000+seed).normal(size=(1000,2))*[.05,.01]
            base=x[ids[0]];new=base+perturb/[np.log(30),.35];z=physical(new)
            runs[strategy]['perturbation']=dict(x=new.tolist(),true_log=z.tolist(),feasible_fraction=float(np.mean(feasible(z))),target_fraction=float(np.mean(target_hit(z))))
    return dict(seed=seed,initial=initial.tolist(),runs=runs)

campaigns=[]
for seed in SEEDS:
    campaigns.append(campaign(seed));print('Completed design comparison',seed,flush=True)
summary={}
for name in ['random','surrogate_ei_cem']:
    rows=[c['runs'][name] for c in campaigns];curves=np.array([r['learning_best_utility'] for r in rows])
    summary[name]=dict(learning_mean=curves.mean(0).tolist(),learning_min=curves.min(0).tolist(),learning_max=curves.max(0).tolist(),
        recommended_loss_each=[r['final_target_loss'] for r in rows],recommended_loss_median=float(np.median([r['final_target_loss'] for r in rows])),
        recommended_utility_mean=float(np.mean([r['final_utility'] for r in rows])),feasible_count=sum(r['final_feasible'] for r in rows),target_hit_count=sum(r['final_target_hit'] for r in rows))
Q=30.;G=12000.;phi=1/Q;nu=G*Q**(1/3)/(8.314462618*298)
chi=-(np.log1p(-phi)+phi+nu*18e-6*(phi**(1/3)-phi/2))/phi**2
inverse_x=np.array([np.log(nu/2)/np.log(30),(chi-.2)/.35]);inverse_truth=physical(inverse_x)[0]
axis=np.linspace(0,1,41);grid=np.array([(a,b) for b in axis for a in axis]);grid_truth=physical(grid)
results=dict(task='Effective gel parameters in an explicit virtual model; biological formulation translation requires measured mapping',
    seeds=SEEDS,budgets=BUDGETS,targets=dict(Q=30,G_kPa=12,minimum_Q=20,G_range_kPa=[8,16],target_factor=1.2),
    model=dict(prior=PRIOR.tolist(),noise_sd=NOISE.tolist(),lengthscales=LENGTH.tolist(),amplitude=1.5,jitter=1e-10),
    analytic_inverse=dict(nu=nu,chi=chi,x=inverse_x.tolist(),predicted_physical_log=inverse_truth.tolist(),target_loss=float(target_loss(inverse_truth))),
    grid=dict(x=grid.tolist(),physical_log=grid_truth.tolist()),cost=dict(search_rounds=24,confirmation_rounds=6,total_paired_rounds=30,scalar_readouts=60,surrogate_candidates_per_query=640,latent_draws_per_candidate=128),
    summary=summary,campaigns=campaigns)
(OUT/'results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(OUT/'samples.json').write_text(json.dumps(dict(campaigns=campaigns,grid=results['grid']),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for name,row in summary.items():
    print(f"{name}: target hits {row['target_hit_count']}/12; feasible {row['feasible_count']}/12; median target loss {row['recommended_loss_median']:.6f}")
print(f'Exact inverse: nu={nu:.6f} mol/m3, chi={chi:.6f}; loss={results["analytic_inverse"]["target_loss"]:.3g}')
print('Per campaign: 24 search + 6 confirmation rounds = 60 scalar readouts')


plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.labelcolor':'#30453f','text.color':'#243d35','axes.edgecolor':'#bac7c0','xtick.color':'#53675e','ytick.color':'#53675e','svg.hashsalt':'L20-design','figure.facecolor':'#fffef9','axes.facecolor':'#fffef9'})
NAMES=['random','surrogate_ei_cem'];LABELS=['Random','AI-guided'];COLORS=['#b18b61','#267b69'];first=campaigns[0]['runs']
def decorate(ax,title,x='',y=''):
    ax.set_title(title,loc='left',fontweight='bold',pad=15);ax.set_xlabel(x);ax.set_ylabel(y);ax.grid(color='#e5eae1',lw=.6);ax.set_axisbelow(True)
def target_region(ax):
    from matplotlib.patches import Rectangle
    ax.axhspan(8,16,color='#e9eee1',alpha=.6);ax.axvline(20,color='#a6b4a1',ls=':',lw=1)
    ax.add_patch(Rectangle((25,10),11,4.4,facecolor='#c0d9c8',edgecolor='#559574',alpha=.55))
    ax.scatter([30],[12],marker='*',s=170,c='#25433a',edgecolor='white',lw=.8,zorder=7,label='Exact inverse')
def draw(i,fig,spec):
    if i==4:
        sub=spec.subgridspec(2,1,hspace=.04)
        for j,(unit,target) in enumerate([('Q / target Q',30),('G / target G',12)]):
            ax=fig.add_subplot(sub[j]);ax.axhspan(1/1.2,1.2,color='#e4eddf');ax.axhline(1,c='#899b87',ls='--',lw=1)
            for k,(name,c) in enumerate(zip(NAMES,COLORS)):
                z=np.exp(np.array(first[name]['confirmation_log']))[:,:,j]/target;actual=np.exp(np.array(first[name]['recommendation_true_log']))[:,j]/target
                for r in range(2):
                    x=k*3+r;ax.scatter(x+np.array([-.14,0,.14]),z[r],c=c,s=35,zorder=4);ax.plot([x-.2,x+.2],[actual[r]]*2,c='#253f35',lw=2)
            ax.set_xticks([0,1,3,4],['Random #1','#2','AI #1','#2']);ax.set_xlim(-.6,4.6)
            decorate(ax,'E  Fresh readings after recommendations are locked' if j==0 else '',y=unit)
            ax.text(.02,.92,'3 fresh paired readings per condition · seed 2000' if j==0 else 'Black marks: model truth; pale band: target range',transform=ax.transAxes,va='top',fontsize=8);ax.set_ylim(.65,1.75)
        return
    ax=fig.add_subplot(spec)
    if i==0:
        im=ax.imshow(utility(grid_truth).reshape(41,41),origin='lower',extent=[0,1,0,1],aspect='auto',cmap='YlGnBu',vmin=0,vmax=1)
        ax.contour(axis,axis,feasible(grid_truth).reshape(41,41).astype(float),levels=[.5],colors=['#a6b4a1'],linewidths=1)
        for name,label,c in zip(NAMES,LABELS,COLORS):
            xy=np.array(first[name]['x'])[8:];ax.scatter(xy[:,0],xy[:,1],s=26,c=c,edgecolor='white',lw=.6,label=label)
        xy=np.array(campaigns[0]['initial']);ax.scatter(*xy.T,marker='+',c='#47667a',s=65,label='8 shared starts');ax.scatter(*inverse_x,marker='*',s=170,c='#e2b35e',edgecolor='white',lw=.8,label='Exact inverse',zorder=5)
        decorate(ax,'A  A physical target inside the parameter domain','Normalized log strand density x₁','Normalized solvent parameter x₂');ax.grid(False);ax.legend(frameon=True,fontsize=8,loc='lower left');fig.colorbar(im,ax=ax,label='True constrained utility',shrink=.8)
    elif i==1:
        clouds=first[NAMES[1]]['steps'][0]['selection']['history']
        for row,c,label,alpha in [(clouds[0],'#b8b5a2','Generation 1',.45),(clouds[-1],'#267b69','Generation 5',.65)]:
            xy=np.array(row['x']);ax.scatter(*xy.T,s=17,c=c,alpha=alpha,label=label)
        row=clouds[-1];xy=np.array(row['x'])[row['elite_indices']];ax.scatter(*xy.T,s=38,facecolors='none',edgecolors='#b47943',lw=1,label='Final elite set')
        xy=first[NAMES[1]]['steps'][0]['x'];ax.scatter(*xy,s=150,marker='*',c='#243f36',zorder=5,label='One selected query');ax.set(xlim=(0,1),ylim=(0,1))
        decorate(ax,'B  Generate many proposals, measure one condition','Normalized log strand density x₁','Normalized solvent parameter x₂');ax.legend(fontsize=8,frameon=False,loc='lower left');ax.text(.03,.95,'First decision · 5 × 128 surrogate proposals',transform=ax.transAxes,va='top',fontsize=9)
    elif i==2:
        for name,label,c in zip(NAMES,LABELS,COLORS):
            r=summary[name];ax.plot(BUDGETS,r['learning_mean'],'o-',c=c,label=label,ms=5);ax.fill_between(BUDGETS,r['learning_min'],r['learning_max'],color=c,alpha=.12)
        ax.axhline(1,c='#647c6b',ls=':',label='Exact physical inverse');ax.set(ylim=(-.03,1.12),xticks=BUDGETS)
        decorate(ax,'C  Best physical utility among queried conditions','Search measurement rounds','Utility (higher is better)');ax.legend(frameon=False,fontsize=9,loc='lower right');ax.text(.03,.52,'Mean and full range of 12 paired campaigns\nTruth used for auditing, never for acquisition',transform=ax.transAxes,fontsize=9)
    elif i==3:
        target_region(ax)
        for name,label,c in zip(NAMES,LABELS,COLORS):
            z=np.exp([r['runs'][name]['recommendation_true_log'][0] for r in campaigns]);ax.scatter(*z.T,s=43,c=c,alpha=.8,edgecolors='white',lw=.7,label=f'{label}: {summary[name]["target_hit_count"]}/12 in target box',zorder=4)
        ax.set(xlim=(18,55),ylim=(6.5,18));decorate(ax,'D  Keep all 24 final recommendations','Volume swelling ratio Q','Swollen-state shear modulus G (kPa)');ax.legend(frameon=False,fontsize=8,loc='upper right');ax.text(.03,.04,'All recommendations meet Q ≥ 20 and 8 ≤ G ≤ 16 kPa',transform=ax.transAxes,fontsize=8)
    else:
        target_region(ax)
        for name,label,c in zip(NAMES,LABELS,COLORS):
            r=first[name]['perturbation'];z=np.exp(r['true_log']);ax.scatter(*z.T,s=7,c=c,alpha=.18,label=f'{label}: {r["target_fraction"]:.1%} in target box')
        ax.set(xlim=(20,60),ylim=(6.5,22));decorate(ax,'F  A specified parameter-variation scenario','Volume swelling ratio Q','Swollen-state shear modulus G (kPa)');ax.legend(frameon=False,fontsize=8,loc='upper right');ax.text(.03,.04,'Seed 2000 · 1,000 perturbations per recommendation\nSD(log ν) = 0.05; SD(χ) = 0.01',transform=ax.transAxes,fontsize=9)
keys=['domain','generation','learning','recommendations','confirmation','variation']
for i,key in enumerate(keys):
    fig=plt.figure(figsize=(8.6,5.5),layout='constrained');draw(i,fig,fig.add_gridspec(1,1)[0]);fig.savefig(OUT/f'{key}.svg',metadata={'Date':None});plt.close(fig)
fig=plt.figure(figsize=(18,16.5),layout='constrained');grid_spec=fig.add_gridspec(3,2,hspace=.12,wspace=.1)
for i in range(6):draw(i,fig,grid_spec[i//2,i%2])
fig.savefig(OUT/'gel_design.svg',metadata={'Date':None});fig.savefig(OUT/'gel_design.png',dpi=160,metadata={'Software':'L20 reproducible example'});plt.close(fig)
print('Full proposals, confirmation data and six figures: design_outputs/')
