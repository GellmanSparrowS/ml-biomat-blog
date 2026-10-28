"""分子组成与环境条件：学习独立位点模型的净电荷响应。

运行：python example.py；依赖：numpy、matplotlib。
教学数据由指定的酸碱平衡模型生成，加上已知尺度的随机噪声。
比较组成模型、条件RBF回归和生成模型本身；温度固定为298 K。
"""
from pathlib import Path
from fractions import Fraction
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT = Path('environment_outputs')
OUT.mkdir(exist_ok=True)
SEED = 20261024
PKA_ACID, PKA_BASE = 4.2, 9.5
CENTERS = np.linspace(4.5, 9.5, 11)
WIDTH, PENALTY, NOISE = .65, 1e-5, .01
GREEN, GOLD, BLUE = '#14786b', '#bc7041', '#406e9c'
plt.rcParams.update({
    'font.family': 'sans-serif', 'font.sans-serif': ['Microsoft YaHei', 'DejaVu Sans'],
    'font.size': 14, 'axes.titlesize': 13, 'axes.spines.top': False,
    'axes.spines.right': False, 'axes.edgecolor': '#a7b9b2',
    'axes.labelcolor': '#24423c', 'text.color': '#24423c',
    'xtick.color': '#536c63', 'ytick.color': '#536c63',
    'figure.facecolor': '#fcfaf5', 'axes.facecolor': '#fcfaf5',
    'svg.fonttype': 'path', 'svg.hashsalt': str(SEED),
})


def ionization(ph):
    """酸性位点带-1的比例，碱性位点带+1的比例。"""
    ph = np.asarray(ph)
    acid = 1 / (1 + 10.0 ** (PKA_ACID - ph))
    base = 1 / (1 + 10.0 ** (ph - PKA_BASE))
    return acid, base


def charge(f_acid, f_base, ph):
    a, b = ionization(ph)
    return f_base * b - f_acid * a  # q/(N e)，无量纲


def design(f_acid, f_base, ph, conditional):
    basic = np.column_stack([np.ones(len(ph)), f_acid, f_base])
    if not conditional:
        return basic
    # 固定中心和宽度。每个钟形函数看一个pH邻域。
    phi = np.exp(-.5 * ((ph[:, None] - CENTERS) / WIDTH) ** 2)
    # 乘上组成比例：相同环境对不同组成可以产生不同响应。
    return np.column_stack([basic, f_acid[:, None] * phi, f_base[:, None] * phi])


def ridge(x, y):
    # 最小化平均平方误差 + PENALTY * 权重平方和；不惩罚偏置。
    diagonal = np.ones(x.shape[1])
    diagonal[0] = 0
    return np.linalg.solve(x.T @ x / len(y) + PENALTY * np.diag(diagonal),
                           x.T @ y / len(y))


def main():
    rng = np.random.default_rng(SEED)
    compositions, seen = [], set()
    while len(compositions) < 320:
        n = int(rng.integers(50, 201))
        a, b, neutral = rng.multinomial(n, rng.dirichlet([2, 2, 4]))
        key = (Fraction(int(a), n), Fraction(int(b), n))
        if key not in seen and a > 0 and b > 0:
            seen.add(key)
            compositions.append([n, int(a), int(b)])
    compositions = np.array(compositions)
    grid = np.linspace(3, 11, 33)
    group = np.repeat(np.arange(320), len(grid))
    ph = np.tile(grid, 320)
    counts = compositions[group]
    fa, fb = counts[:, 1] / counts[:, 0], counts[:, 2] / counts[:, 0]
    exact = charge(fa, fb, ph)
    measured = exact + rng.normal(0, NOISE, len(exact))
    heldout = rng.choice(320, 80, replace=False)
    new_group = np.isin(group, heldout)
    in_range = (ph >= 4.5) & (ph <= 9.5)
    train = ~new_group & in_range
    interpolation, extrapolation = new_group & in_range, new_group & ~in_range
    weights, predictions = {}, {}
    for name, conditional in [('composition', False), ('conditional', True)]:
        x = design(fa, fb, ph, conditional)
        weights[name] = ridge(x[train], measured[train])
        predictions[name] = x @ weights[name]
    predictions['equilibrium'] = exact.copy()
    metrics = {}
    for name, mask in [('new_composition', interpolation), ('new_composition_new_ph', extrapolation)]:
        metrics[name] = {key: {
            'mae_to_exact': float(np.mean(np.abs(value[mask] - exact[mask]))),
            'rmse_to_observation': float(np.sqrt(np.mean((value[mask] - measured[mask]) ** 2))),
        } for key, value in predictions.items()}
    # 两端电离极限、总电荷范围及独立组划分。
    check_fa, check_fb = .3, .2
    limit_error = max(abs(charge(check_fa, check_fb, -20) - check_fb),
                      abs(charge(check_fa, check_fb, 30) + check_fa))
    checks = {
        'train_test_group_overlap': len(set(group[train]) & set(group[new_group])),
        'unique_composition_groups': len(seen),
        'low_high_ph_limit_error': float(limit_error),
        'charge_bounds': bool(np.all(exact >= -fa) and np.all(exact <= fb)),
        'acid_fraction_at_pka': float(ionization(PKA_ACID)[0]),
        'base_fraction_at_pka': float(ionization(PKA_BASE)[1]),
    }
    assert checks['train_test_group_overlap'] == 0 and len(seen) == 320
    assert limit_error < 1e-10 and checks['charge_bounds']
    assert checks['acid_fraction_at_pka'] == checks['base_fraction_at_pka'] == .5
    # 选用测试组之一展示完整响应曲线，不参与调参。
    probe_group = int(heldout[0])
    probe = group == probe_group
    residual_ph = []
    for p in grid:
        mask = new_group & (ph == p)
        residual_ph.append([float(p), *[float(np.mean(np.abs(predictions[key][mask] - exact[mask])))
                                      for key in ['composition', 'conditional', 'equilibrium']]])
    result = {
        'seed': SEED, 'source': 'specified_independent_site_model_with_gaussian_noise',
        'pka_acid': PKA_ACID, 'pka_base': PKA_BASE, 'temperature_K': 298,
        'noise_sd_charge_per_unit': NOISE, 'n_groups': 320,
        'n_train': int(train.sum()), 'n_test_in': int(interpolation.sum()),
        'n_test_out': int(extrapolation.sum()),
        'centers': CENTERS.tolist(), 'basis_width': WIDTH, 'ridge_penalty': PENALTY,
        'weights': {k:v.tolist() for k,v in weights.items()},
        'metrics': metrics, 'checks': checks,
        'probe': {'group': probe_group, 'counts_N_acid_base': compositions[probe_group].tolist(),
                  'ph': ph[probe].tolist(), 'exact': exact[probe].tolist(),
                  'observation': measured[probe].tolist(),
                  'prediction': {k:v[probe].tolist() for k,v in predictions.items()}},
        'mae_by_ph': residual_ph,
    }
    records = []
    for i in range(len(ph)):
        split = 'train' if train[i] else 'test_in' if interpolation[i] else 'test_out' if extrapolation[i] else 'unused'
        records.append({'group':int(group[i]), 'N':int(counts[i,0]),
            'n_acid':int(counts[i,1]), 'n_base':int(counts[i,2]), 'pH':float(ph[i]),
            'exact_charge_per_unit':float(exact[i]), 'noisy_observation':float(measured[i]), 'split':split})
    (OUT/'samples.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
    (OUT/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')

    def shade(ax):
        ax.axvspan(3, 4.5, color='#e9dac7', alpha=.55)
        ax.axvspan(9.5, 11, color='#e9dac7', alpha=.55)
        ax.set_xlim(3, 11)

    def fractions(ax):
        dense = np.linspace(3, 11, 300)
        a, b = ionization(dense)
        ax.plot(dense, a, color=GREEN, lw=2, label='酸性位点：负电比例')
        ax.plot(dense, b, color=GOLD, lw=2, label='碱性位点：正电比例')
        ax.scatter([PKA_ACID, PKA_BASE], [.5, .5], c=[GREEN, GOLD], s=55, zorder=3)
        ax.axhline(.5, color='#bac8bd', lw=1, ls=':')
        ax.set(xlabel='pH', ylabel='带相应电荷的位点比例', ylim=(-.03,1.05),
               title='A  两类位点，响应方向不同')
        ax.legend(frameon=False, fontsize=10, loc='lower right')

    def response(ax):
        shade(ax)
        ax.scatter(ph[probe], measured[probe], c='#9caea3', s=18, label='带噪观测')
        for key,color,ls,name in [('equilibrium',GREEN,'-','平衡参照'),
            ('conditional',BLUE,'--','条件回归'),('composition',GOLD,':','组成回归')]:
            ax.plot(ph[probe],predictions[key][probe],color=color,ls=ls,lw=2,label=name)
        ax.set(xlabel='pH（米色为训练范围外）',ylabel='平均电荷 q/(N e)',
               title='B  一个完整留出组成的响应曲线')
        ax.legend(frameon=False,fontsize=10,ncol=2)

    def surface(ax):
        pp, ff = np.meshgrid(np.linspace(3,11,150),np.linspace(0,.65,100))
        zz = charge(ff,.2,pp)
        im = ax.pcolormesh(pp,ff,zz,cmap='BrBG',vmin=-.65,vmax=.65,shading='auto',rasterized=True)
        ax.contour(pp,ff,zz,levels=[0],colors=['#333f3a'],linewidths=[1.1])
        ax.set(xlabel='pH',ylabel='酸性位点比例',title='C  组成与环境共同决定响应')
        cb=ax.figure.colorbar(im,ax=ax,pad=.025);cb.set_label('q/(N e)')

    def comparison(ax):
        # 图上抽稀便于看清，误差使用全部测试例子。
        take=np.flatnonzero(interpolation)[::6]
        ax.scatter(exact[take],predictions['composition'][take],color=GOLD,s=15,alpha=.55,label='只看组成')
        ax.scatter(exact[take],predictions['conditional'][take],color=BLUE,s=12,alpha=.55,label='加入pH')
        lo,hi=exact[interpolation].min(),exact[interpolation].max()
        ax.plot([lo,hi],[lo,hi],color=GREEN,lw=1.5)
        ax.set(xlabel='平衡参照 q/(N e)',ylabel='模型预测 q/(N e)',title='D  新组成、已见过的pH范围')
        ax.legend(frameon=False,fontsize=10)

    def errors(ax):
        names=['composition','conditional','equilibrium']
        pos=np.arange(3)
        for split,offset,color,label in [('new_composition',-.18,GREEN,'pH范围内'),
                 ('new_composition_new_ph',.18,GOLD,'pH范围外')]:
            values=[metrics[split][k]['mae_to_exact'] for k in names]
            bars=ax.bar(pos+offset,values,width=.34,color=color,label=label)
            for bar,value in zip(bars,values):
                ax.text(bar.get_x()+bar.get_width()/2,value+.002,f'{value:.3f}',ha='center',fontsize=10)
        ax.set(xticks=pos,xticklabels=['组成回归','条件回归','平衡参照'],
               ylabel='对无噪平衡值的MAE',title='E  留出新条件，重新检查误差')
        ax.set_ylim(0,max(metrics['new_composition_new_ph'][k]['mae_to_exact'] for k in names)*1.3)
        ax.legend(frameon=False,fontsize=10)

    def error_curve(ax):
        shade(ax)
        a=np.array(residual_ph)
        for col,color,label in [(1,GOLD,'组成回归'),(2,BLUE,'条件回归')]:
            ax.plot(a[:,0],a[:,col],color=color,lw=2,label=label)
        ax.set(xlabel='pH（米色为训练范围外）',ylabel='新组成上的平均绝对误差',
               title='F  看误差在哪些条件下积累')
        ax.legend(frameon=False,fontsize=10)

    panels=[('fractions',fractions),('response',response),('surface',surface),
            ('comparison',comparison),('errors',errors),('error_curve',error_curve)]
    for name,draw in panels:
        fig,ax=plt.subplots(figsize=(6.6,4.6),layout='constrained');draw(ax)
        fig.savefig(OUT/(name+'.svg'),metadata={'Date':None});plt.close(fig)
    fig,axes=plt.subplots(3,2,figsize=(14,14),layout='constrained')
    for (_,draw),ax in zip(panels,axes.ravel()):draw(ax)
    fig.savefig(OUT/'environment_diagnostics.svg',metadata={'Date':None})
    fig.savefig(OUT/'environment_diagnostics.png',dpi=180);plt.close(fig)
    print(f'训练例子 {train.sum()}；范围内测试 {interpolation.sum()}；范围外测试 {extrapolation.sum()}')
    for split,rows in metrics.items():
        for key,value in rows.items():
            print(f'{split} / {key}: MAE(平衡值)={value["mae_to_exact"]:.5f}, RMSE(带噪观测)={value["rmse_to_observation"]:.5f}')
    print('训练/测试共有组成组数：',checks['train_test_group_overlap'])
    print('结果与完整样本已保存至 environment_outputs')


if __name__=='__main__':
    main()
