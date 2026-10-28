"""Learn future conditional means from Gaussian-chain trajectories.
Python + NumPy + Matplotlib. Reduced units: b0=1, kBT=1, zeta0=1,
t0=zeta0*b0**2/kBT=1, spring constant ks=3*kBT/b0**2.
The trajectories are model simulations; experimental history is cited in the text.
"""
from pathlib import Path
import base64
import json
import zlib
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT=Path("dynamics_outputs"); OUT.mkdir(exist_ok=True)
M=16; KS=3.; KT=1.; ZETA=1.; DT=.5
STEPS=1024; TOTAL=448; HISTORY=8
HORIZONS=np.array([1,4,16,64])
COLORS=["#247968","#c46c46","#596d99","#b3945d"]
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":11,
    "axes.spines.top":False,"axes.spines.right":False,
    "axes.labelcolor":"#273b36","text.color":"#273b36",
    "svg.hashsalt":"ai4s-L08","savefig.facecolor":"#fffdf8"})


def chain_modes(beads):
    p=np.arange(1,beads)
    eigenvalue=4*np.sin(np.pi*p/(2*beads))**2
    basis=np.sqrt(2/beads)*np.cos((np.arange(beads)[:,None]+.5)*p*np.pi/beads)
    variance=KT/(KS*eigenvalue)
    end_coeff=basis[-1]-basis[0]
    return eigenvalue,basis,variance,end_coeff


LAM,BASIS,VAR,END=chain_modes(M)
END_VARIANCE=float((END**2)@VAR)


def simulate(count,friction,seed,keep_modes=False):
    rng=np.random.default_rng(seed)
    decay=np.exp(-KS*LAM*DT/friction)
    noise=np.sqrt(VAR*(1-decay**2))
    modes=rng.normal(size=(count,M-1))*np.sqrt(VAR)
    trace=np.empty((count,STEPS))
    first=np.empty((count,STEPS)) if keep_modes else None
    for t in range(STEPS):
        trace[:,t]=modes@END/np.sqrt(END_VARIANCE)
        if keep_modes: first[:,t]=modes[:,0]/np.sqrt(VAR[0])
        if t+1<STEPS:
            modes=modes*decay+rng.normal(size=modes.shape)*noise
    return trace,first


def correlation(lag_frames,friction=ZETA):
    lag=np.asarray(lag_frames)
    weights=END**2*VAR/END_VARIANCE
    return np.sum(weights*np.exp(-abs(lag)[...,None]*DT*KS*LAM/friction),axis=-1)


def measured_correlation(traces,lag):
    if lag==0:return 1.
    return float(np.sum(traces[:,:-lag]*traces[:,lag:])/np.sum(traces[:,:-lag]**2))


def make_windows(traces):
    times=np.arange(HISTORY-1,STEPS-HORIZONS.max(),8)
    x=traces[:,times[:,None]-np.arange(HISTORY)[None,:]]
    y=traces[:,times[:,None]+HORIZONS[None,:]]
    return x,y,times


def physics_prediction_weights(horizons):
    past=np.arange(HISTORY)
    covariance=correlation(past[:,None]-past[None,:])
    cross=correlation(past[:,None]+np.asarray(horizons)[None,:])
    weights=np.linalg.solve(covariance,cross)
    residual_variance=1-np.sum(cross*weights,axis=0)
    return weights,residual_variance,covariance,cross


def main():
    trace,first_mode=simulate(TOTAL,ZETA,808,keep_modes=True)
    slow,_=simulate(256,4.,809)
    # Split independent trajectories BEFORE creating windows.
    train=np.arange(256); valid=np.arange(256,320); test=np.arange(320,TOTAL)
    x,y,origins=make_windows(trace)
    xtr=x[train].reshape(-1,HISTORY); ytr=y[train].reshape(-1,len(HORIZONS))
    candidates=[]
    for reg in [0.,1e-5,1e-3,.01,.1]:
        w=np.linalg.solve(xtr.T@xtr/len(xtr)+reg*np.eye(HISTORY),xtr.T@ytr/len(xtr))
        loss=float(np.mean((x[valid]@w-y[valid])**2))
        candidates.append((loss,reg,w))
    validation_loss,regularization,weights=min(candidates,key=lambda row:row[0])
    rho=float(np.sum(trace[train,:-1]*trace[train,1:])/np.sum(trace[train,:-1]**2))
    physical_weights,physical_variance,_,_=physics_prediction_weights(HORIZONS)
    prediction={"persistence":np.repeat(x[test,:,0,None],len(HORIZONS),axis=-1),
        "AR1_recursive":x[test,:,0,None]*rho**HORIZONS,
        "direct_history8":x[test]@weights,"same_history_physics":x[test]@physical_weights}
    metrics={};per_trajectory_errors={}
    for name,values in prediction.items():
        # Windows overlap in time; uncertainty is calculated across whole trajectories.
        errors=np.mean((values-y[test])**2,axis=1)
        per_trajectory_errors[name]=errors
        metrics[name]={"mse":errors.mean(axis=0).tolist(),
            "standard_error":(errors.std(axis=0,ddof=1)/np.sqrt(len(test))).tolist()}

    # A fixed test trajectory and origin selected before examining its future.
    example_id=320; origin=256; future=np.arange(1,65)
    history=trace[example_id,origin-np.arange(HISTORY)]
    fw,fv,cov,cross=physics_prediction_weights(future)
    conditional_mean=history@fw
    residual_cov=correlation(future[:,None]-future[None,:])-cross.T@fw
    factor=np.linalg.cholesky(residual_cov+1e-12*np.eye(len(future)))
    alternatives=conditional_mean+np.random.default_rng(1808).normal(size=(5,len(future)))@factor.T

    # Same physical observation duration, different recording intervals.
    strides=np.array([1,2,4,8,16,32])
    measured=[]; theoretical=[]; mode_measured=[]
    for stride in strides:
        sparse=trace[test,::stride]; sparse_mode=first_mode[test,::stride]
        rr=measured_correlation(sparse,1); rm=measured_correlation(sparse_mode,1)
        assert 0<rr<1 and 0<rm<1
        measured.append(-stride*DT/np.log(rr))
        theoretical.append(-stride*DT/np.log(correlation(stride)))
        mode_measured.append(-stride*DT/np.log(rm))
    equilibrium={}
    for name,values in [("zeta1",trace),("zeta4",slow)]:
        moments=np.mean(values**2,axis=1)
        mean=float(moments.mean()); se=float(moments.std(ddof=1)/np.sqrt(len(moments)))
        equilibrium[name]={"mean":float(values.mean()),"second_moment":mean,"second_moment_se":se,
                           "second_moment_z":(mean-1)/se}
        assert abs((mean-1)/se)<5

    # Independent force/mode and stationary-covariance algebra checks.
    lap=np.diag(np.r_[1,np.full(M-2,2),1])-np.diag(np.ones(M-1),1)-np.diag(np.ones(M-1),-1)
    mode_error=float(np.max(abs(lap@BASIS-BASIS*LAM)))
    orthogonal_error=float(np.max(abs(BASIS.T@BASIS-np.eye(M-1))))
    decay=np.exp(-KS*LAM*DT/ZETA)
    stationary_error=float(np.max(abs(VAR*decay**2+VAR*(1-decay**2)-VAR)))
    assert mode_error<1e-12 and orthogonal_error<1e-12 and stationary_error<1e-12
    assert abs(END_VARIANCE-(M-1)*KT/KS)<1e-12
    paired_difference=per_trajectory_errors['AR1_recursive']-per_trajectory_errors['direct_history8']
    results={"model":"3D Gaussian vector-spring Rouse chain; observed endpoint x projection; stationary start; free ends",
        "units":{"length":"b0","energy":"kBT0","friction":"zeta0","time":"t0=zeta0*b0^2/(kBT0)"},
        "parameters":{"M":M,"ks":KS,"kBT":KT,"zeta":ZETA,"dt":DT,"steps":STEPS},
        "tau1":float(ZETA/(KS*LAM[0])),"end_x_variance":END_VARIANCE,
        "split":{"train_ids":train.tolist(),"validation_ids":valid.tolist(),"test_ids":test.tolist()},
        "history":HISTORY,"window_stride":8,"windows_per_trajectory":len(origins),
        "horizons_frames":HORIZONS.tolist(),"horizons_time":(HORIZONS*DT).tolist(),
        "AR1_coefficient":rho,"direct_weights":weights.tolist(),"physical_weights":physical_weights.tolist(),
        "validation_choices":[{"lambda":reg,"mse":loss} for loss,reg,_ in candidates],
        "selected_regularization":regularization,"selected_validation_mse":validation_loss,
        "theoretical_residual_variance":physical_variance.tolist(),"test_metrics":metrics,
        "paired_AR1_minus_direct":{"mean":paired_difference.mean(axis=0).tolist(),
            "standard_error":(paired_difference.std(axis=0,ddof=1)/np.sqrt(len(test))).tolist()},
        "sampling":{"stride":strides.tolist(),"apparent_tau_observed":measured,
            "apparent_tau_theory":theoretical,"pure_mode_tau_observed":mode_measured},
        "equilibrium":equilibrium,"checks":{"mode_operator_error":mode_error,
            "orthonormal_basis_error":orthogonal_error,"stationary_variance_identity_error":stationary_error},
        "reference_information":"Physical predictor receives exactly the same eight scalar observations as the learned predictor."}
    # Full float64 trajectories are compressed losslessly to keep the download small.
    encoded=base64.b64encode(zlib.compress(trace.astype('<f8').tobytes(),level=9)).decode('ascii')
    samples={"trajectory_encoding":"zlib compressed base64, little-endian float64, row-major",
        "trajectory_shape":list(trace.shape),"trajectory_data":encoded,
        "window_origins":origins.tolist(),"horizons_frames":HORIZONS.tolist(),
        "example":{"trajectory_id":example_id,"origin":origin,"past":history.tolist(),
            "future_actual":trace[example_id,origin+future].tolist(),
            "conditional_mean":conditional_mean.tolist(),"conditional_variance":fv.tolist(),
            "conditional_sample_futures":alternatives.tolist()},
        "per_test_trajectory_mse":{key:val.tolist() for key,val in per_trajectory_errors.items()}}
    (OUT/'samples.json').write_text(json.dumps(samples,indent=2),encoding='utf-8')
    (OUT/'results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')

    def panel(ax,name):
        if name=='forecast':
            ft=future*DT
            ax.fill_between(ft,conditional_mean-1.6448536269514722*np.sqrt(fv),
                conditional_mean+1.6448536269514722*np.sqrt(fv),color=COLORS[0],alpha=.13,label='90% pointwise conditional band')
            for i,alternative in enumerate(alternatives[:3]):
                ax.plot(ft,alternative,c=COLORS[2],alpha=.22,lw=1,label='Other possible futures' if i==0 else None)
            ax.plot(ft,trace[example_id,origin+future],c=COLORS[1],lw=1.5,label='Observed test future')
            ax.plot(ft,conditional_mean,c=COLORS[0],lw=2,label='Physical conditional mean')
            ax.scatter(HORIZONS*DT,history@weights,c='#263a35',s=36,zorder=5,label='Learned mean (4 horizons)')
            ax.scatter([0],[history[0]],c='#263a35',s=24)
            ax.set(xlabel='Future time / t0',ylabel='Normalized endpoint projection s',title='A  A mean forecast and possible futures')
            ax.legend(frameon=False,fontsize=8,loc='lower right')
        elif name=='correlation':
            lag=np.arange(129)
            for fr,values,c in [(1.,trace[test],COLORS[0]),(4.,slow,COLORS[1])]:
                ax.plot(lag*DT,correlation(lag,fr),c=c,label=f'Exact, friction = {fr:g}')
                picks=np.arange(0,129,8)
                ax.scatter(picks*DT,[measured_correlation(values,int(q)) for q in picks],facecolors='none',edgecolors=c,s=25)
            ax.axhline(0,c='#b9c1b8',lw=1)
            ax.set(xlabel='Time separation / t0',ylabel='Normalized autocorrelation',title='B  Same equilibrium size, different speed')
            ax.legend(frameon=False,fontsize=9)
        elif name=='modes':
            sizes=np.arange(4,65)
            for order,c in zip([1,2,4],COLORS):
                use=sizes>order
                tau=ZETA/(4*KS*np.sin(np.pi*order/(2*sizes[use]))**2)
                ax.plot(sizes[use],tau,c=c,label=f'Mode p = {order}')
            ax.plot(sizes,ZETA*sizes**2/(KS*np.pi**2),'--',c=COLORS[3],label='Large-M approximation, p = 1')
            ax.set(xscale='log',yscale='log',xlabel='M / beads',ylabel='Relaxation time / t0',title='C  Large-scale shapes relax more slowly')
            ax.legend(frameon=False,fontsize=9)
        elif name=='weights':
            im=ax.imshow(weights.T,aspect='auto',cmap='BrBG',
                norm=matplotlib.colors.TwoSlopeNorm(vmin=-.1,vcenter=0,vmax=.75))
            ax.set_xticks(range(HISTORY),[str(j) for j in range(HISTORY)])
            ax.set_yticks(range(4),[str(t) for t in HORIZONS*DT])
            ax.set(xlabel='Past observation / frames before present',ylabel='Forecast horizon / t0',title='D  Learned temporal weights')
            for i in range(4):
                for j in range(HISTORY):
                    displayed=0. if abs(weights[j,i])<.005 else weights[j,i]
                    ax.text(j,i,f'{displayed:.2f}',ha='center',va='center',fontsize=9,color='white' if weights[j,i]>.5 else '#273b36')
            ax.figure.colorbar(im,ax=ax,label='Regression weight',shrink=.8)
        elif name=='errors':
            labels=['Keep current value','Learned AR(1), iterated','Learned 8-value history','Same-history physical mean']
            for (key,metric),label,c in zip(metrics.items(),labels,COLORS):
                ax.errorbar(HORIZONS*DT,metric['mse'],yerr=np.array(metric['standard_error'])*2,
                    marker='o',capsize=3,c=c,label=label,ls='--' if key=='same_history_physics' else '-')
            ax.plot(HORIZONS*DT,physical_variance,'k:',lw=1.5,label='Exact conditional residual variance')
            ax.set(xscale='log',xlabel='Forecast horizon / t0',ylabel='Test mean squared error',title='E  Prediction error grows with horizon')
            ax.legend(frameon=False,fontsize=8,loc='upper left')
        else:
            ax.plot(strides*DT,theoretical,c=COLORS[0],label='Endpoint: exact lag-dependent value')
            ax.scatter(strides*DT,measured,c=COLORS[0],label='Endpoint: sampled estimate',s=26)
            ax.axhline(ZETA/(KS*LAM[0]),c=COLORS[2],ls='--',label='Slowest mode: exact relaxation time')
            ax.scatter(strides*DT,mode_measured,c=COLORS[2],marker='s',s=26,label='Slowest mode: sampled estimate')
            ax.set(xscale='log',xlabel='Recording interval / t0',ylabel='Single-exponential apparent time / t0',title='F  What time does a one-step fit measure?')
            ax.legend(frameon=False,fontsize=8,loc='lower right')
        if name!='weights':ax.grid(alpha=.15)

    keys=['forecast','correlation','modes','weights','errors','sampling']
    for name in keys:
        fig,ax=plt.subplots(figsize=(6.7,5),layout='constrained',facecolor='#fffdf8')
        panel(ax,name);fig.savefig(OUT/(name+'.svg'),metadata={'Date':None});plt.close(fig)
    fig,axes=plt.subplots(3,2,figsize=(16,17),layout='constrained',facecolor='#fffdf8')
    for ax,name in zip(axes.flat,keys):panel(ax,name)
    fig.savefig(OUT/'dynamics_diagnostics.svg',metadata={'Date':None})
    fig.savefig(OUT/'dynamics_diagnostics.png',dpi=160,metadata={'Software':'Matplotlib'});plt.close(fig)
    print('Independent trajectories, train / validation / test: 256 / 64 / 128')
    print('Each trajectory: 1024 frames; input history: 8; windows per trajectory:',len(origins))
    print('Exact slowest relaxation time:',round(results['tau1'],4),'t0')
    print('Selected regularization:',regularization,'; learned AR(1) coefficient:',round(rho,5))
    for name,metric in metrics.items(): print(name,'MSE:',np.round(metric['mse'],5).tolist())
    print('Exact residual variance:',np.round(physical_variance,5).tolist())
    print('Equilibrium second moments, friction 1 and 4:',[round(equilibrium[k]['second_moment'],4) for k in equilibrium])
    print('Saved full compressed trajectories, fitted weights, six panels and checks.')


if __name__=='__main__':main()
