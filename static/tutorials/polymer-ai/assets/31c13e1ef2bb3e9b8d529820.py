"""Entropic elasticity and curve-to-parameter learning.

Requires NumPy and Matplotlib. The DNA numerical subset is embedded below.
Synthetic data: long-chain Marko-Siggia interpolation, kBT=4.11 pN nm.
Observed extensions have independent Gaussian noise with sigma=10 nm.
All curves for one parameter pair remain in the same data partition.
"""
from pathlib import Path
from math import comb
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT=Path("elasticity_outputs")
OUT.mkdir(exist_ok=True)
KT=4.11                    # pN nm, prescribed model/analysis thermal scale
SIGMA=10.0                 # nm, independent synthetic extension noise
SEED=606
COLORS=["#887a69","#cd6c47","#247b69","#304d77"]
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":14,
    "axes.spines.top":False,"axes.spines.right":False,"axes.labelsize":14,
    "axes.titlesize":15,"legend.fontsize":11,"svg.hashsalt":"L06-elasticity",
    "savefig.facecolor":"#fffdf8"})

# LUMICKS (2024), DOI 10.5281/zenodo.12668419, CC BY 4.0.
# Original FD curve has 1267 time-aligned rows. Select rows 0,8,16,...,1264
# plus final row1266, in time order. Distance1: um -> nm; Trap2: total force pN.
# Values below are measurements, not generated from the teaching model.
DNA_DATA = np.array([
    [1507.554534, 0.01045498505],
    [1523.136068, 0.08885946445],
    [1535.541275, 0.1687685737],
    [1547.031289, 0.04142682294],
    [1564.944785, 0.03013699975],
    [1580.633798, 0.1710104162],
    [1599.832833, 0.2555742697],
    [1611.640918, 0.2611575828],
    [1619.359454, 0.172676309],
    [1637.234512, 0.1825457563],
    [1651.416951, 0.2767096909],
    [1663.529555, 0.09165729488],
    [1676.144339, 0.09389412018],
    [1690.963765, 0.3921573974],
    [1705.344865, 0.3151567484],
    [1719.389995, 0.2414734165],
    [1737.162577, 0.1116167701],
    [1746.686195, 0.3078744522],
    [1758.624625, 0.2281664175],
    [1773.532496, 0.2663851125],
    [1786.222186, 0.2270622483],
    [1796.577336, 0.3339478803],
    [1810.825296, 0.2413859999],
    [1825.157082, 0.2718138058],
    [1836.909443, 0.217689204],
    [1851.809182, 0.1611735374],
    [1862.406028, 0.2703681853],
    [1874.097214, 0.07652316169],
    [1886.472474, 0.2114218607],
    [1900.826269, 0.1449865622],
    [1915.830096, 0.4356262262],
    [1924.691503, 0.3071022763],
    [1937.784975, 0.1723059021],
    [1952.731717, 0.286821541],
    [1962.803235, 0.252511253],
    [1981.52594, 0.2096999973],
    [1990.67831, 0.2428496321],
    [2002.316077, 0.1494624249],
    [2019.073389, 0.2644964021],
    [2027.833499, 0.3735661086],
    [2043.104416, 0.1299659277],
    [2055.940192, 0.4409992036],
    [2070.024288, 0.3098122365],
    [2083.318213, 0.4836215197],
    [2096.116547, 0.3330418343],
    [2106.282228, 0.5648385224],
    [2119.697231, 0.3634308418],
    [2133.847631, 0.4148978598],
    [2150.500628, 0.4289832871],
    [2161.047878, 0.5170297211],
    [2174.50172, 0.5954173016],
    [2189.15149, 0.4544984685],
    [2204.392974, 0.5213618599],
    [2217.59961, 0.5820380183],
    [2229.518985, 0.6031777796],
    [2246.194418, 0.8759342631],
    [2255.860666, 0.5522027276],
    [2271.066459, 0.6739869944],
    [2282.656399, 0.7050620859],
    [2297.500535, 0.6861668245],
    [2307.963368, 0.9191275541],
    [2323.601013, 0.8673508165],
    [2337.358996, 1.019640667],
    [2352.367426, 0.9743398238],
    [2364.193478, 1.24158943],
    [2380.658924, 1.157390868],
    [2395.97708, 1.218444628],
    [2405.674579, 1.298080123],
    [2418.248302, 1.552148888],
    [2433.788794, 1.196310683],
    [2445.213539, 1.175867846],
    [2456.817424, 1.625276605],
    [2462.096883, 1.66573742],
    [2480.437948, 1.959157439],
    [2490.22269, 2.108187995],
    [2508.032596, 2.29843103],
    [2518.30837, 2.551807612],
    [2525.951681, 2.602889598],
    [2544.65005, 2.65824777],
    [2551.285402, 2.963749443],
    [2565.952081, 3.28134667],
    [2571.725021, 3.611023673],
    [2583.924447, 3.99099344],
    [2595.372515, 4.297163709],
    [2605.513594, 4.686616351],
    [2614.617598, 5.282804865],
    [2620.126816, 5.628527138],
    [2633.883887, 6.053970808],
    [2643.131742, 6.75757233],
    [2650.081229, 7.311676405],
    [2657.743555, 7.950219231],
    [2666.031066, 8.728832102],
    [2669.196243, 9.471160433],
    [2678.890608, 10.37366703],
    [2686.524497, 11.22826411],
    [2690.370437, 12.1790347],
    [2698.504033, 13.04508965],
    [2702.780681, 14.04463534],
    [2705.31928, 14.92266881],
    [2714.506998, 15.89771119],
    [2718.704968, 17.0274443],
    [2723.28215, 18.00026112],
    [2728.487208, 19.21627224],
    [2732.136944, 20.11133906],
    [2735.604938, 21.33507719],
    [2740.100266, 22.53171821],
    [2745.62744, 23.64217255],
    [2749.147666, 24.88696251],
    [2752.538689, 26.0251913],
    [2757.071741, 27.04885791],
    [2762.950896, 28.48879533],
    [2764.012533, 29.58709585],
    [2769.712702, 30.81326221],
    [2770.355888, 31.70166611],
    [2772.276864, 32.91303383],
    [2777.22185, 34.1580418],
    [2781.053545, 35.39139773],
    [2783.8933, 36.73083354],
    [2787.074834, 37.85867963],
    [2794.013887, 39.23008715],
    [2794.58562, 40.29165576],
    [2801.619321, 41.54880707],
    [2801.822473, 42.96044768],
    [2805.216603, 44.28649504],
    [2810.686538, 45.54748891],
    [2817.107268, 46.63191962],
    [2815.394326, 48.11835243],
    [2822.600217, 49.24243661],
    [2828.210121, 50.43548283],
    [2835.293831, 51.78914243],
    [2836.091015, 53.050245],
    [2842.18347, 54.15289598],
    [2852.222431, 55.36057004],
    [2852.747486, 56.49801074],
    [2860.413174, 57.25527057],
    [2866.657441, 58.42017796],
    [2874.544328, 59.28254273],
    [2880.697058, 60.22567337],
    [2895.81331, 60.59442648],
    [2902.435861, 61.522872],
    [2911.342985, 62.4946558],
    [2924.708487, 62.70705063],
    [2924.949902, 64.1106122],
    [2942.705501, 64.20267266],
    [2950.188725, 64.81263955],
    [2956.598732, 65.32539],
    [2966.673789, 63.55397612],
    [2969.825373, 63.21359917],
    [2969.453152, 63.05145617],
    [2968.777814, 63.18882922],
    [2967.418946, 63.14275629],
    [2972.776499, 63.09865436],
    [2967.329544, 63.30396642],
    [2969.016752, 63.26432442],
    [2965.801886, 63.02874795],
    [2968.625615, 63.13315603],
    [2968.800594, 63.11083838],
    [2968.625598, 62.90583761],
    [2967.675089, 63.02169566],
    [2968.452555, 63.08041695],
], dtype=float)


def phi(x):
    """Dimensionless Marko-Siggia force for fractional extension x."""
    return 1/(4*(1-x)**2)-.25+x


def extension_fraction(force, lp):
    """Invert the monotonic force relation by bounded bisection."""
    scaled=np.asarray(force)*np.asarray(lp)/KT
    lo=np.zeros_like(scaled);hi=np.ones_like(scaled)*(1-1e-9)
    for _ in range(45):
        mid=(lo+hi)/2
        below=phi(mid)<scaled
        lo=np.where(below,mid,lo);hi=np.where(below,hi,mid)
    return (lo+hi)/2


def physical_fit(observations, force, lp_grid):
    """Profile lp; solve the best L analytically at each candidate lp."""
    shape=extension_fraction(force[None,:],lp_grid[:,None])
    results=[];ranges=[];profiles=[]
    for observed in observations:
        lengths=(shape@observed)/np.sum(shape**2,axis=1)
        cost=np.sum((lengths[:,None]*shape-observed)**2,axis=1)/SIGMA**2
        best=int(np.argmin(cost));delta=cost-cost[best]
        accepted=delta<=4.0   # diagnostic cost contour, not a calibrated probability
        results.append([lengths[best],lp_grid[best]])
        ranges.append([lp_grid[accepted][0],lp_grid[accepted][-1],
                       bool(accepted[0] or accepted[-1])])
        profiles.append(delta)
    return np.array(results),np.array(ranges),np.array(profiles)


def predict(parameters,x):
    a,b,c,d=parameters
    return np.tanh(x@a+b)@c+d


def objective(parameters,x,y):
    a,b,c,d=parameters
    h=np.tanh(x@a+b);error=h@c+d-y
    derivative=2*error/error.size
    hidden=(derivative@c.T)*(1-h*h)
    return float(np.mean(error**2)),[x.T@hidden,hidden.sum(0),h.T@derivative,derivative.sum(0)]


def train_network(x,y,x_valid,y_valid,seed):
    rng=np.random.default_rng(seed)
    pars=[rng.normal(0,.13,(24,32)),np.zeros(32),
          rng.normal(0,.12,(32,2)),np.zeros(2)]
    first=[np.zeros_like(p) for p in pars];second=[p.copy() for p in first]
    best_loss=float("inf");best=None;history=[];best_step=0
    for t in range(1,2501):
        loss,grads=objective(pars,x,y)
        for j,g in enumerate(grads):
            first[j]=.9*first[j]+.1*g;second[j]=.999*second[j]+.001*g*g
            pars[j]-=.003*(first[j]/(1-.9**t))/(np.sqrt(second[j]/(1-.999**t))+1e-8)
        if t==1 or t%25==0:
            validation=float(np.mean((predict(pars,x_valid)-y_valid)**2))
            history.append([t,loss,validation])
            if validation<best_loss:
                best_loss=validation;best=[p.copy() for p in pars];best_step=t
    return best,history,best_step


def fit_real_dna():
    """Force-residual fit to the declared 0.2--5 pN measurement subset."""
    z,f=DNA_DATA.T
    keep=(f>=.2)&(f<=5)
    # At fixed L, force = a*phi(z/L), with a=kBT/lp.
    L_grid=np.linspace(max(z[keep])+1,3500,10000)
    shape=phi(z[keep][None,:]/L_grid[:,None])
    amplitude=(shape@f[keep])/np.sum(shape*shape,axis=1)
    cost=np.mean((amplitude[:,None]*shape-f[keep])**2,axis=1)
    best=int(np.argmin(cost))
    return {"L_nm":float(L_grid[best]),"lp_nm":float(KT/amplitude[best]),
        "force_rmse_pN":float(np.sqrt(cost[best])),"fit_points":int(keep.sum()),
        "force_window_pN":[.2,5.],"kBT_pN_nm":KT,"offsets":"fixed zero",
        "input_points":len(f),"doi":"10.5281/zenodo.12668419","credit":"LUMICKS (2024), CC BY 4.0"}


def verify_math():
    counts=[comb(4,j) for j in range(5)]
    assert counts==[1,4,6,4,1] and sum(counts)==16
    x=np.linspace(0,.99,200)
    assert phi(0)==0 and np.all(np.diff(phi(x))>0)
    assert abs(phi(1e-6)/1e-6-1.5)<1e-5
    inverse=extension_fraction(np.geomspace(.01,5,40),50)
    inverse_error=float(np.max(abs(KT/50*phi(inverse)-np.geomspace(.01,5,40))))
    assert inverse_error<1e-9
    # Independently perturb every weight in a tiny two-output network.
    r=np.random.default_rng(10)
    p=[r.normal(size=(3,4)),r.normal(size=4),r.normal(size=(4,2)),r.normal(size=2)]
    a=r.normal(size=(7,3));b=r.normal(size=(7,2));_,gradient=objective(p,a,b)
    grad_error=0.
    for j,parameter in enumerate(p):
        for ix in np.ndindex(parameter.shape):
            original=parameter[ix];eps=1e-6
            parameter[ix]=original+eps;up=objective(p,a,b)[0]
            parameter[ix]=original-eps;down=objective(p,a,b)[0]
            parameter[ix]=original
            grad_error=max(grad_error,abs((up-down)/(2*eps)-gradient[j][ix]))
    assert grad_error<1e-7
    return {"four_step_counts":counts,"inverse_force_max_error_pN":inverse_error,
            "gradient_max_error":grad_error,"small_extension_slope":float(phi(1e-6)/1e-6)}


def main():
    rng=np.random.default_rng(SEED)
    count=1000
    truth=np.c_[rng.uniform(2000,4500,count),rng.uniform(25,80,count)]
    order=rng.permutation(count)
    train,valid,test=order[:650],order[650:800],order[800:]
    assert not(set(train)&set(valid) or set(train)&set(test) or set(valid)&set(test))
    partitions=np.array(["test"]*count,dtype=object)
    partitions[train]="train";partitions[valid]="validation"
    log_target=np.log(truth)   # numerical ratios to1nm for both positive lengths
    ymean,ysd=log_target[train].mean(0),log_target[train].std(0)
    yt=(log_target-ymean)/ysd
    lp_grid=np.geomspace(5,250,1500)
    windows={"wide":[.01,5.],"narrow":[.01,.03]}
    all_runs={};samples=[];results={"seed":SEED,"noise_sigma_nm":SIGMA,
        "kBT_pN_nm":KT,"train_groups":650,"validation_groups":150,"test_groups":200,
        "parameter_order":["L_nm","lp_nm"],"parameter_bounds_nm":[[2000,4500],[25,80]],
        "profile_lp_search_nm":[5,250],"profile_threshold_delta_cost":4,
        "profile_interpretation":"diagnostic cost range; boundary-touching values are flagged",
        "target_standardization":{"mean":ymean.tolist(),"std":ysd.tolist()},
        "checks":verify_math(),"windows":{}}
    for name,limits in windows.items():
        force=np.geomspace(*limits,24)
        exact=truth[:,0,None]*extension_fraction(force[None,:],truth[:,1,None])
        observed=exact+rng.normal(0,SIGMA,exact.shape)
        mean,sd=observed[train].mean(0),observed[train].std(0)
        x=(observed-mean)/sd
        design=np.c_[np.ones(len(train)),x[train]]
        penalty=np.eye(25)*.01;penalty[0,0]=0
        ridge=np.linalg.solve(design.T@design/len(train)+penalty,design.T@yt[train]/len(train))
        weights,history,best_step=train_network(x[train],yt[train],x[valid],yt[valid],SEED+len(name))
        phys,ranges,profiles=physical_fit(observed[test],force,lp_grid)
        predictions={"mean":np.tile(truth[train].mean(0),(len(test),1)),
            "ridge":np.exp((np.c_[np.ones(len(test)),x[test]]@ridge)*ysd+ymean),
            "network":np.exp(predict(weights,x[test])*ysd+ymean),"physics":phys}
        metrics={}
        for model,prediction in predictions.items():
            error=100*np.abs(prediction-truth[test])/truth[test]
            metrics[model]={"median_relative_error_percent":np.median(error,axis=0).tolist(),
                "mean_absolute_error_nm":np.mean(abs(prediction-truth[test]),axis=0).tolist()}
        results['windows'][name]={"force_pN":force.tolist(),"metrics":metrics,
            "input_standardization":{"mean":mean.tolist(),"std":sd.tolist()},
            "ridge_weights":ridge.tolist(),"network_weights":[p.tolist() for p in weights],
            "network_best_step_from_validation":best_step,"history":history,
            "profile_median_width_nm":float(np.median(ranges[:,1]-ranges[:,0])),
            "profile_boundary_touch_count":int(ranges[:,2].sum())}
        test_position={int(group):j for j,group in enumerate(test)}
        for group in range(count):
            row={"group":group,"split":str(partitions[group]),"window":name,
                "L_nm":float(truth[group,0]),"lp_nm":float(truth[group,1]),
                "extensions_nm":observed[group].tolist()}
            if group in test_position:
                j=test_position[group]
                row['predictions_nm']={key:value[j].tolist() for key,value in predictions.items()}
                row['profile_lp_range_nm']=ranges[j,:2].tolist()
                row['profile_touches_search_bound']=bool(ranges[j,2])
            samples.append(row)
        all_runs[name]={'predictions':predictions,'ranges':ranges,'profiles':profiles,'force':force,'observed':observed}
    real=fit_real_dna();results['real_dna']=real
    results['checks']['no_parameter_group_overlap']=True
    (OUT/'results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
    (OUT/'samples.json').write_text(json.dumps(samples,indent=2),encoding='utf-8')
    np.savetxt(OUT/'dna_selected_data.csv',DNA_DATA,delimiter=',',header='distance_nm,total_force_trap2_pN',comments='')

    def panel(ax,key):
        if key=='counts':
            ends=np.arange(-4,5,2);counts=np.array([comb(4,j) for j in range(5)])
            ax.bar(ends,counts,width=1.2,color=COLORS[2])
            for end,c in zip(ends,counts):ax.text(end,c+.12,str(c),ha='center',fontsize=14)
            ax.set(xticks=ends,xlabel='Endpoint / segment length',ylabel='Number of conformations',
                title='A  Four steps: 16 possible paths',ylim=(0,7))
        elif key=='force_law':
            frac=np.linspace(0,.92,200)
            ax.plot(frac,1.5*frac,c=COLORS[0],ls='--',label='Small-extension limit')
            ax.plot(frac,phi(frac),c=COLORS[2],label='WLC interpolation')
            ax.set(xlabel='Extension / contour length',ylabel=r'$f\ell_p/(k_BT)$',title='B  Finite contour, rising force',ylim=(0,12))
            ax.legend(frameon=False)
        elif key=='parameters':
            for model,c in [('network',COLORS[1]),('physics',COLORS[2])]:
                ax.scatter(truth[test,1],all_runs['wide']['predictions'][model][:,1],s=19,alpha=.65,color=c,label=model)
            ax.plot([25,80],[25,80],c=COLORS[0],ls='--')
            ax.set(xlabel='True persistence length / nm',ylabel='Estimated persistence length / nm',title='C  New parameter pairs, wide window')
            ax.legend(frameon=False)
        elif key=='comparison':
            names=['mean','ridge','network','physics']
            for j,name in enumerate(windows):
                errors=[results['windows'][name]['metrics'][key2]['median_relative_error_percent'][1] for key2 in names]
                ax.bar(np.arange(4)+(j-.5)*.36,errors,width=.36,color=[COLORS[2],COLORS[1]][j],label=name+' force range')
            ax.set_xticks(range(4),['Mean','Ridge','Network','Physics'])
            ax.set(ylabel='Median persistence-length error / %',title='D  Same 24 measurements, new range')
            ax.legend(frameon=False)
        elif key=='profiles':
            for name,c in [('wide',COLORS[2]),('narrow',COLORS[1])]:
                ax.plot(lp_grid,all_runs[name]['profiles'][0],color=c,label=name)
            ax.axhline(4,color=COLORS[0],ls=':',label='Diagnostic cost rise = 4')
            ax.axvline(truth[test[0],1],color=COLORS[3],ls='--',label='Generating parameter')
            ax.set(xlabel='Candidate persistence length / nm',ylabel='Cost above minimum',title='E  How wide is the fitting valley?',ylim=(0,15),xlim=(5,140))
            ax.legend(frameon=False)
        elif key=='dna':
            z,f=DNA_DATA.T;keep=(f>=.2)&(f<=5)
            ax.scatter(z[~keep]/1000,f[~keep],s=13,color='#b6b8b1',label='Outside fit range')
            ax.scatter(z[keep]/1000,f[keep],s=19,color=COLORS[1],label='Measured: 0.2--5 pN')
            grid=np.linspace(z[keep].min(),z[keep].max(),150)
            ax.plot(grid/1000,KT/real['lp_nm']*phi(grid/real['L_nm']),color=COLORS[2],label='Specified WLC fit')
            ax.set(xlabel='Distance / micrometre',ylabel='Total force / pN',title='F  Public DNA measurements',ylim=(0,6),xlim=(1.5,2.85))
            ax.legend(frameon=False)
            ax.text(.03,.96,'LUMICKS (2024) / CC BY 4.0',transform=ax.transAxes,va='top',fontsize=10)
        ax.grid(alpha=.16)
    keys=['counts','force_law','parameters','comparison','profiles','dna']
    for key in keys:
        fig,ax=plt.subplots(figsize=(6.8,5.1),layout='constrained',facecolor='#fffdf8')
        panel(ax,key);fig.savefig(OUT/(key+'.svg'),metadata={'Date':None});plt.close(fig)
    fig,axes=plt.subplots(3,2,figsize=(16,17),layout='constrained',facecolor='#fffdf8')
    for ax,key in zip(axes.flat,keys):panel(ax,key)
    fig.savefig(OUT/'elasticity_diagnostics.svg',metadata={'Date':None})
    fig.savefig(OUT/'elasticity_diagnostics.png',dpi=150,metadata={'Software':'Matplotlib'});plt.close(fig)
    print('Parameter groups: 650 train / 150 validation / 200 test; each has both force windows.')
    for name in windows:
        print(name, 'median lp errors (%)', {key:round(v['median_relative_error_percent'][1],3) for key,v in results['windows'][name]['metrics'].items()})
        print('  selected training step:',results['windows'][name]['network_best_step_from_validation'],
              '; diagnostic range touches search bounds:',results['windows'][name]['profile_boundary_touch_count'])
    print('DNA: points used =',real['fit_points'],'; fitted lp (nm) =',round(real['lp_nm'],3),
          '; fitted L (nm) =',round(real['L_nm'],3),'; force RMSE (pN) =',round(real['force_rmse_pN'],4))
    print('Gradient check:',f"{results['checks']['gradient_max_error']:.2e}")
    print('Saved full curves, fitted models and six result panels.')


if __name__=='__main__':
    main()
