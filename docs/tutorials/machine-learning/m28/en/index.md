# Projects: turn an improvement into reproducible evidence

Source: https://ml-biomat.com/tutorials/machine-learning/m28/en/
Language: en

Why does moving a digit by one pixel change recognition? Use a complete controlled study to connect reproduction, ablation, statistics, and experimental writing.

## 1. Why does a nearly perfect recognizer struggle with a one-pixel move?

A postal digit written in the middle of a box is recognized almost every time. Move the same digit slightly to the right, and the recognizer gets almost half the images wrong. The digit remains the same, and no ink disappears; only its position changes. This observation is a useful starting point for a research project. Has the model learned the shape, or does it rely too heavily on strokes occurring at particular coordinates? Should we build a deeper network, expose the model to translated training images, or inspect the evaluation procedure first? A productive investigation begins with an observable difference and separates its possible explanations.

This chapter conducts a complete experiment using public handwritten digits. A baseline correctly classifies 448 of 450 centered test images, giving 99.56% accuracy. When centered, left-shifted, right-shifted, upward-shifted, and downward-shifted images receive equal weight, average accuracy falls to 62.27%. Training with translation augmentation raises this five-position average to 98.00%, while centered-image accuracy becomes 98.67%. The result contains both a large improvement and a smaller tradeoff. Our task is to identify where the improvement comes from, which inputs it concerns, and how to connect the program, measurements, and explanation into evidence another person can inspect.

Reproducibility initiatives in machine learning address this connection. Pineau and colleagues' 2021 report describes the NeurIPS 2019 reproducibility program, which combined code sharing, a reproduction challenge, and a checklist of experimental information. Code describes how a calculation is performed; data and settings establish which question that calculation answers. When reading a paper, begin with a concrete claim, locate its supporting experiment, and trace that experiment back to the split, transformation, and metric. A statement about recognizing shifted digits then has an identifiable relationship to both a figure and a computational procedure.

The experiment follows the idea of broadening training experience through image transformations, explained in Dive into Deep Learning. We use a kernel SVM to keep the intervention small and controllable. This is an investigation of the augmentation mechanism under the explicit settings given here. Reproducing a particular number from a published paper is a related task: it additionally requires matching that paper's data and evaluation protocol. Both activities can be useful, provided the question in the title matches the experiment being conducted. Learning to state that question precisely is part of doing the research.

## 2. Before training, decide what one observation represents

The experiment uses the 1,797 images supplied by scikit-learn's digits loader. Each image has 8 by 8 pixels and a label from zero to nine. Original pixel values range from zero to sixteen and represent counts of ink pixels within small regions of a normalized digit. Dividing by sixteen produces inputs between zero and one. We place each image in the center of a 10 by 10 zero-valued canvas, leaving a one-pixel border. A one-pixel translation moves the image into this border without cropping any ink. This simple construction protects the experimental idea: change position while retaining the observed shape.

![Controlled translations of the same digit](https://ml-biomat.com/static/tutorials/machine-learning/figures/894c1558e36f4852d45d8049.svg?v=894c1558e36f)

Figure 1Three actual test digits at five positions on 10×10 canvases, grayscale 0–1. Border padding preserves all ink during a one-pixel move. Data: Alpaydin and Kaynak, UCI Optical Recognition of Handwritten Digits, CC BY 4.0. This figure displays transformed dataset observations.

The underlying data are Alpaydin and Kaynak's Optical Recognition of Handwritten Digits, distributed through UCI under CC BY 4.0. The original collection used different writers for its training and test groups; the scikit-learn loader supplies a 1,797-image subset. Our experiment makes a new class-stratified split within that subset: 450 test images and 1,347 development images. The resulting scores describe held-out images in this collection. A project concerned with previously unseen writers should obtain writer identities and split by writer. Ten digits from one person carry a different kind of diversity from digits supplied by ten different people.

During parameter selection, 270 development images become validation observations and the other 1,077 become training observations. We split original images first and create their translated views afterward. Consequently, every version of a digit remains on the same side of each split. Augmenting first and randomly splitting the resulting rows could put a left-shifted image in training and its right-shifted counterpart in testing. The evaluation would then concern another view of an already encountered observation. The unit of sampling determines the population to which a result speaks, so the implementation must preserve that unit throughout preprocessing and evaluation.

A concise data card records these decisions: what a row represents, how labels were obtained, what pixel values mean, which observations belong to each split, whether a transformation preserves the label, and how the data can be obtained and reused. The same questions apply to other modalities. Audio observations may share a speaker or a recording; demand measurements may share a date and location; several document questions may depend on one source document. A useful data card makes those relationships visible. Its purpose is to help the next researcher understand the observations, rather than to accumulate administrative descriptions disconnected from the experiment.

## 3. Does augmentation help because of new positions or simply more rows?

We compare three training conditions. The first uses centered images. The second repeats each centered image five times without modification. The third uses the centered image and four one-pixel translations. The second condition is a particularly informative control: it has as many training rows as the third but contains no additional position information. All three conditions share the development and test observations, the RBF kernel, and the same candidate parameter values. This design lets us distinguish the effects of adding rows from the effects of exposing the learner to meaningful variation in where the strokes appear.

There is another variable hidden in the objective. Soft-margin SVMs penalize the sum of training losses. Repeating every observation five times multiplies that sum by five, changing its balance against the regularizer if C stays fixed. We therefore divide the C passed to SVC by five for both the repeated and augmented conditions. Each view receives less weight, while the total weight associated with an original image remains unchanged. Multiclass SVC applies the same convention within its binary subproblems. Controlling a comparison requires understanding the optimization objective, as well as counting the number of rows in a training file.

$$
J_k(w)=\tfrac12\|w\|^2+\frac{C_0}{k}\sum_{i=1}^{n}\sum_{j=1}^{k}\ell_{ij}(w),\qquad \ell_{ij}=\max(0,1-y_i f_w(x_{ij}))
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/acdad4257c29c3f9dad2a348.svg) | Weights in kernel feature space and the binary decision function including its intercept; inputs and scores are dimensionless here. |
| ![Formula](https://ml-biomat.com/static/agent-math/19ba377343847499549adf7a.svg) | Original training-image count, views per image, image index and view index; unitless counts. |
| ![Formula](https://ml-biomat.com/static/agent-math/31fd8bf45874cdf65e568268.svg) | View j of image i and its ±1 label within a binary subproblem; the 100-dimensional pixel input is normalized to 0–1. |
| ![Formula](https://ml-biomat.com/static/agent-math/fa309d8becb78768250709af.svg) | Base loss weight, hinge loss and objective, all dimensionless here; the C passed to SVC equals C0/k. |
| ![Formula](https://ml-biomat.com/static/agent-math/17e4be483413f8a681b9b712.svg) | Squared weight norm, measured in the kernel feature space. |

If one image has loss 0.4 and C0=10, its contribution is 4. Five identical copies with C=2 contribute 2×5×0.4=4; keeping C=10 would contribute 20. Augmented views generally have different losses. C0/k preserves the total weight per original image while teaching those views. Multiclass SVC combines binary subproblem decisions.

The kernel parameter gamma is fixed at 0.05, and the base C is selected from 1, 3, and 10. Each condition chooses its C by average validation accuracy across the five positions; a tie keeps the smaller candidate. The selected setting is then fitted to all 1,347 development images and evaluated on the 450 reserved test images. Three inner-split seeds, 11, 29, and 47, change which development images serve as validation observations. The outer test set remains fixed. Parameter selection belongs to the method being evaluated, so the baseline receives the same opportunity to select a setting as the proposed intervention.

Equal search counts and equal computation budgets answer different questions. Every condition tries three values of C here, but the augmented kernel problem contains more rows and costs more to solve. A study of performance under a fixed computing budget should give methods a common budget and select settings within it. A study of whether position variation contributes useful information first holds the learner and total loss weight per original observation fixed. Either comparison can be well designed. The important decision is which resource or mechanism the research question asks us to control, and how the reported experiment implements that decision.

## 4. Run the complete experiment, then read the comparisons

The following script performs splitting, parameter selection for all three conditions, development-set refitting, individual predictions, paired statistics, and plotting. The dataset is bundled with scikit-learn, so execution requires no separate data download. The output splits.json records original image indices, results.csv stores validation and test measurements, and predictions.npz retains predictions for every image and position. These files let a reader trace a plotted number back to the observations it summarizes. The script also records a fingerprint of the images and labels, allowing two runs to check that they used the same underlying array rather than merely the same dataset name.

### Complete experiment: three controls, individual predictions, and paired bootstrap

The script produces splits, result tables, numerical summaries, and three figure groups. Test split seed2801, inner-selection seeds11/29/47, and bootstrap seed2802 are fixed.

```
"""A paired, controlled study of translation augmentation on public digits.

Dataset: E. Alpaydin and C. Kaynak, UCI Optical Recognition of Handwritten
Digits, DOI 10.24432/C50P49, CC BY 4.0. load_digits contains 1,797 images.
This study uses a new image-level split, not the original writer-level split.
"""
import argparse, csv, hashlib, json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

SHIFTS=[(0,0),(0,-1),(0,1),(-1,0),(1,0)]
FAMILIES=['original','copies','shifted']

def canvases(images,shifts):
    """Pad to 10x10, translate at most one pixel, never crop ink."""
    result=[]
    for dy,dx in shifts:
        a=np.zeros((len(images),10,10))
        a[:,1+dy:9+dy,1+dx:9+dx]=images/16.0
        result.append(a.reshape(len(images),100))
    return np.concatenate(result)

def training_data(images,labels,family):
    shifts=SHIFTS if family=='shifted' else [(0,0)]*(5 if family=='copies' else 1)
    return canvases(images,shifts),np.tile(labels,len(shifts)),len(shifts)

def score(pred,y):return float(np.mean(pred==y))

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--language',choices=['zh','en'],default='en');args=p.parse_args()
    out=args.output;out.mkdir(parents=True,exist_ok=True);zh=args.language=='zh'
    plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'] if zh else ['DejaVu Sans'], 'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','axes.unicode_minus':False,'figure.facecolor':'white'})
    labels={'original':'原样本' if zh else 'Original','copies':'原样本复制5份' if zh else 'Five identical copies','shifted':'5种位置增广' if zh else 'Five translated views'}
    colors={'original':'#286d90','copies':'#a6afb4','shifted':'#bc6b31'}
    ds=load_digits();images=ds.images;y=ds.target;indices=np.arange(len(y))
    development,test=train_test_split(indices,test_size=450,random_state=2801,stratify=y)
    test_views=canvases(images[test],SHIFTS);test_y=np.tile(y[test],5)
    # Fixed gamma depends on input dimensions, not on an examined test distribution.
    # C/replicas keeps the sum-loss weight per original observation unchanged.
    candidates=[1.0,3.0,10.0];seeds=[11,29,47];records=[];predictions={};split_records=[];selection=[]
    for seed in seeds:
        train,valid=train_test_split(development,test_size=270,random_state=seed,stratify=y[development])
        split_records.append({'seed':seed,'train':train.tolist(),'validation':valid.tolist(),'test':test.tolist()})
        valid_x=canvases(images[valid],SHIFTS);valid_y=np.tile(y[valid],5)
        for family in FAMILIES:
            xtr,ytr,k=training_data(images[train],y[train],family)
            chosen=None
            for c in candidates:
                model=SVC(C=c/k,kernel='rbf',gamma=.05,tol=1e-5,cache_size=180)
                model.fit(xtr,ytr);acc=score(model.predict(valid_x),valid_y)
                selection.append({'seed':seed,'family':family,'C_base':c,'validation_accuracy':acc})
                if chosen is None or acc>chosen[0]:chosen=(acc,c)
            xdev,ydev,k=training_data(images[development],y[development],family)
            model=SVC(C=chosen[1]/k,kernel='rbf',gamma=.05,tol=1e-5,cache_size=180).fit(xdev,ydev)
            pred=model.predict(test_views).reshape(5,len(test));predictions[(seed,family)]=pred
            view_accuracy=(pred==y[test]).mean(axis=1)
            records.append({'seed':seed,'family':family,'C_base':chosen[1],'validation_accuracy':chosen[0],'center_accuracy':float(view_accuracy[0]),'five_view_accuracy':float(view_accuracy.mean()),'view_accuracy':view_accuracy.tolist(),'support_vectors':int(model.n_support_.sum())})
    base=predictions[(11,'original')]==y[test];aug=predictions[(11,'shifted')]==y[test]
    difference=aug.mean(axis=0)-base.mean(axis=0)
    rng=np.random.default_rng(2802);boot=difference[rng.integers(0,len(test),(3000,len(test)))].mean(axis=1)
    interval=np.quantile(boot,[.025,.975])
    right=2;a=base[right];b=aug[right]
    paired={'both_correct':int(np.sum(a&b)),'base_only':int(np.sum(a&~b)),'aug_only':int(np.sum(~a&b)),'both_wrong':int(np.sum(~a&~b))}
    summary={'n_images':len(y),'development':len(development),'test':len(test),'inner_train':1077,'inner_validation':270,'seeds':seeds,'candidates':candidates,'gamma':.05,'records':records,'selection':selection,'paired_right_shift_seed11':paired,'bootstrap_unit':'original test image, carrying all five views','delta_five_views_seed11':float(difference.mean()),'bootstrap_interval_seed11':interval.tolist(),'bootstrap_replicates':3000,'views_per_image':5,'ink_sum_error':float(np.max(np.abs(test_views.sum(axis=1)-np.tile(images[test].sum(axis=(1,2))/16,5)))),'development_test_overlap':len(set(development)&set(test)),'duplicate_prediction_disagreements':int(sum(np.sum(predictions[(s,'original')]!=predictions[(s,'copies')]) for s in seeds))}
    (out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8')
    (out/'splits.json').write_text(json.dumps(split_records),encoding='utf8')
    np.savez_compressed(out/'predictions.npz',test_indices=test,labels=y[test],**{f'{s}_{f}':v for (s,f),v in predictions.items()})
    with (out/'results.csv').open('w',newline='',encoding='utf8') as f:
        keys=['seed','family','C_base','validation_accuracy','center_accuracy','five_view_accuracy','support_vectors'];writer=csv.DictWriter(f,fieldnames=keys);writer.writeheader();writer.writerows({k:r[k] for k in keys} for r in records)
    (out/'data_fingerprint.txt').write_text(hashlib.sha256(images.astype('<f8').tobytes()+y.astype('<i8').tobytes()).hexdigest()+'\n',encoding='ascii')
    def save(fig,name):
        fig.savefig(out/f'{name}-{args.language}.svg',bbox_inches='tight');plt.close(fig)
    # Original images make the controlled intervention visible.
    fig,ax=plt.subplots(3,5,figsize=(11,6.6),layout='constrained')
    names=['中心','左移','右移','上移','下移'] if zh else ['Centered','Left','Right','Up','Down']
    chosen_images=[test[np.where(y[test]==label)[0][0]] for label in [3,6,8]]
    for row,index in enumerate(chosen_images):
        views=canvases(images[index:index+1],SHIFTS).reshape(5,10,10)
        for j in range(5):
            ax[row,j].imshow(views[j],cmap='gray_r',vmin=0,vmax=1,interpolation='nearest');ax[row,j].set_xticks([]);ax[row,j].set_yticks([])
            for sp in ax[row,j].spines.values():sp.set_visible(False)
            if row==0:ax[row,j].set_title(names[j])
            if j==0:ax[row,j].set_ylabel(('真值 ' if zh else 'Label ')+str(y[index]),fontsize=11)
    save(fig,'views')
    fig,axs=plt.subplots(1,3,figsize=(14,4.3),layout='constrained',gridspec_kw={'width_ratios':[1.3,1,1]})
    matrix=np.array([next(r for r in records if r['seed']==11 and r['family']==f)['view_accuracy'] for f in FAMILIES])
    im=axs[0].imshow(matrix,vmin=0,vmax=1,cmap='YlGnBu',aspect='auto');axs[0].set_xticks(range(5),names,rotation=25);axs[0].set_yticks(range(3),[labels[f] for f in FAMILIES]);axs[0].set_title('各位置正确率：选择划分11' if zh else 'Accuracy by view: selection split 11')
    for i in range(3):
        for j in range(5):axs[0].text(j,i,f'{matrix[i,j]*100:.1f}',ha='center',va='center',color='white' if matrix[i,j]>.65 else '#173d4c',fontsize=9)
    fig.colorbar(im,ax=axs[0],fraction=.045,pad=.02,label='正确率' if zh else 'Accuracy')
    for panel,metric,title in [(axs[1],'center_accuracy','中心图像' if zh else 'Centered images'),(axs[2],'five_view_accuracy','五位置平均' if zh else 'Average over five views')]:
        for s in seeds:
            values=[next(r for r in records if r['seed']==s and r['family']==f)[metric]*100 for f in FAMILIES]
            panel.plot(range(3),values,color='#bac5c9',linewidth=1,zorder=1)
        for i,f in enumerate(FAMILIES):
            values=[r[metric]*100 for r in records if r['family']==f];panel.scatter(np.full(3,i)+np.array([-.06,0,.06]),values,color=colors[f],s=35,zorder=2)
        panel.set_xticks(range(3),[labels[f] for f in FAMILIES],rotation=22,ha='right');panel.set_ylabel('正确率 / %' if zh else 'Accuracy / %');panel.set_ylim(0,102);panel.grid(axis='y',alpha=.15);panel.set_title(title)
    save(fig,'comparison')
    fig=plt.figure(figsize=(13,6.5),layout='constrained');gs=fig.add_gridspec(2,4,height_ratios=[1.1,1])
    ax=fig.add_subplot(gs[0,:2]);ax.hist(boot*100,bins=35,color='#468596',edgecolor='white');ax.axvline(difference.mean()*100,color='#bb6736',linewidth=2);ax.axvline(interval[0]*100,color='#546870',ls='--');ax.axvline(interval[1]*100,color='#546870',ls='--');ax.set_xlabel('增广 − 原样本 / 百分点' if zh else 'Augmented − original / percentage points');ax.set_ylabel('重采样次数' if zh else 'Bootstrap draws');ax.set_title('以原始图像为重采样单位' if zh else 'Resample original images with their five views')
    ax=fig.add_subplot(gs[0,2:]);counts=np.array([[paired['both_correct'],paired['base_only']],[paired['aug_only'],paired['both_wrong']]])
    ax.imshow(counts,cmap='Blues',vmin=0,vmax=450);ax.set_xticks([0,1],['增广正确','增广错误'] if zh else ['Augmented correct','Augmented wrong']);ax.set_yticks([0,1],['基线正确','基线错误'] if zh else ['Baseline correct','Baseline wrong'])
    for i in range(2):
        for j in range(2):ax.text(j,i,str(counts[i,j]),ha='center',va='center',fontsize=20,color='white' if counts[i,j]>225 else '#18384a')
    ax.set_title('同450张右移图像的成对结果' if zh else 'Paired outcomes on the same 450 right-shifted images')
    groups=[np.where(~a&b)[0],np.where(a&~b)[0],np.where(~a&~b)[0],np.where(a&b)[0]]
    names2=['增广修复','增广新错','共同错误','共同正确'] if zh else ['Corrected by augmentation','New augmentation error','Both wrong','Both correct']
    for j,group in enumerate(groups):
        ax=fig.add_subplot(gs[1,j]);ax.set_xticks([]);ax.set_yticks([])
        if len(group):
            idx=group[0];ax.imshow(test_views[right*len(test)+idx].reshape(10,10),cmap='gray_r',vmin=0,vmax=1);ax.set_xlabel(('真值 / 基线 / 增广 = ' if zh else 'True / baseline / augmented = ')+f'{y[test[idx]]} / {predictions[(11,"original")][right,idx]} / {predictions[(11,"shifted")][right,idx]}',fontsize=9)
        else:ax.text(.5,.5,'本组0张' if zh else 'No images in this group',ha='center',va='center',transform=ax.transAxes)
        ax.set_title(names2[j],fontsize=10)
    save(fig,'paired')
    print(json.dumps({'records':records,'delta':summary['delta_five_views_seed11'],'interval':interval.tolist(),'paired':paired,'copies_disagree':summary['duplicate_prediction_disagreements']},ensure_ascii=False))
if __name__=='__main__':main()
```

The heat map separates the five evaluation positions. The baseline is nearly perfect on centered images but reaches only 46.44% after a downward translation. The augmented model stays near 97% to 99% across positions. Thus, most of the improvement occurs on translated inputs, while a few new errors appear on centered inputs. The middle and right panels preserve these two evaluation goals separately. Collapsing all observations into a single number would hide the concrete tradeoff: greater tolerance of position changes with a small decrease in centered-image accuracy. The target application determines which mix of positions deserves the most weight.

![Three training conditions evaluated at different positions](https://ml-biomat.com/static/tutorials/machine-learning/figures/77d14f19d75bca18426d60b4.svg?v=77d14f19d75b)

Figure 2Left: position-specific accuracy on 450 fixed test images after selection split 11; cell values are percentages. Middle/right: centered and five-position accuracy for three inner-selection seeds, with lines linking conditions within a seed. All select C0=10 and predict identically after refitting on the same development set. Points have a small horizontal offset for visibility; they are not independent experimental error bars.

The repeated-image condition and the original condition predict exactly the same classes at all tested positions. Together with the C divided by five control, this result supports attributing the main change to position information. The augmented model's five-position average exceeds the baseline by 35.73 percentage points. A percentage-point difference subtracts two percentages; a relative percentage increase divides that difference by the baseline. Naming the unit prevents ambiguity. Support-vector entries also differ across conditions, at 486, 1,119, and 2,876. Duplicating rows can change how support is represented, so this count should be interpreted alongside the construction of the training data.

Why do the final test points for three selection seeds overlap? All three splits select base C=10. Each selected configuration is then fitted on the same 1,347 development images using the same deterministic SVM, producing the same predicted classes. The seeds vary the inner split; they do not automatically create three independent test experiments. This is an instructive result to retain. A report with several seeds should explain what those seeds change. Studying random initialization requires a learner that uses random initialization; studying observation selection requires different outer splits or a sampling design that explicitly varies the relevant observations.

## 5. Compare two models on the same answer sheet

Two separate average scores discard information about how the models differ on the same images. Among the 450 right-shifted test images, both models answer correctly on 229, the augmented model alone answers correctly on 210, both are wrong on 11, and the baseline alone is correct on none. A two-by-two table makes the origin of the improvement visible. Cases where both models are correct or both are wrong cancel when computing the accuracy difference. The two disagreement groups determine the difference. Pairing also matters statistically because a difficult image is likely to influence both models' outcomes at the same time.

$$
n=n_{11}+n_{10}+n_{01}+n_{00},\quad a_A=\frac{n_{11}+n_{10}}n,\quad a_B=\frac{n_{11}+n_{01}}n,\quad \Delta=a_B-a_A=\frac{n_{01}-n_{10}}n
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/f12c13576bb625453e573142.svg) | Baseline and augmented models compared on identical observations. |
| ![Formula](https://ml-biomat.com/static/agent-math/aeeca924111fd3a75173acfe.svg) | The first subscript indicates whether A is correct, the second whether B is correct; one means correct, zero wrong; nab counts those observations. |
| ![Formula](https://ml-biomat.com/static/agent-math/f524fa4611e4410e9a58920a.svg) | Sample count, two accuracies, and their difference; n>0, accuracies are unitless, and 100Δ is in percentage points. |

With six both-correct, one A-only, three B-only and zero both-wrong observations, n=10. A scores 7/10, B scores 9/10, and the difference is (3−1)/10=0.2, or twenty percentage points. Shared correct outcomes cancel; the disagreement groups determine the difference.

### Experiment: split an improvement into two disagreement groups

The four cells record whether two models answer the same observations correctly. Adjust counts to see the paired accuracies and difference change. Try the ten-image example, then return to the right-shift experiment.

[Figure: Paired outcome matrix and accuracy](https://ml-biomat.com/tutorials/machine-learning/m28/en/#M28-plot)

Counts refer to observations, and the models always face the same set. Augmentation-only successes increase the difference; baseline-only successes decrease it.

The full comparison includes all five positions. For each original image, first average each model's correctness over its five views, then subtract the baseline value from the augmented value. This produces 450 paired differences. When resampling, draw an original image together with all five views; do not treat the 2,250 view-level observations as independent examples. The five views share the same handwriting and therefore carry related errors. The script draws 3,000 bootstrap samples of original images with replacement, recalculating the average difference each time. The resulting distribution displays variation associated with the finite test-image sample under this defined grouping.

$$
d_i=\frac1K\sum_{j=1}^{K}\left[\mathbf1(\widehat y^{B}_{ij}=y_i)-\mathbf1(\widehat y^{A}_{ij}=y_i)\right],\quad\bar d=\frac1n\sum_{i=1}^{n}d_i,\quad\bar d^{*(b)}=\frac1n\sum_{r=1}^{n}d_{I_{br}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/70e731e73bce482ecf0af045.svg) | Original test-image count, positions per image, and corresponding indices; n=450 and K=5 here. |
| ![Formula](https://ml-biomat.com/static/agent-math/811d7e06c9188f193ccfb450.svg) | True class, A/B predictions at position j, and indicator; the indicator is one when its condition holds, zero otherwise, all unitless. |
| ![Formula](https://ml-biomat.com/static/agent-math/01b6557f1746d01716e2e7a4.svg) | Per-image mean difference over positions, its overall average, and bootstrap average b; accuracy differences, multiplied by 100 for percentage points. |
| ![Formula](https://ml-biomat.com/static/agent-math/47b2a5dc5ab32f0013c327f0.svg) | Bootstrap replicate, draw position within it, and an original-image index sampled uniformly with replacement from 1 through n; all views of an image travel together. |

For two image differences 0.2 and 0.6, the original mean is 0.4. Sampling two indices with replacement gives (1,1), (1,2), (2,1), or (2,2), with means 0.2,0.4,0.4,0.6. The full experiment uses 3,000 replicates and the 2.5th/97.5th percentiles for a 95% percentile interval, retaining original images as units.

The 95% percentile bootstrap interval runs from 33.73 to 37.69 percentage points around an estimated difference of 35.73 points. Its meaning follows the resampling operation: variation in test images for these fixed fitted models, preserving each image's five views. A new population of writers, arbitrary rotations, and variation from retraining are separate experimental dimensions. To investigate writers, collect writer identifiers and evaluate by that grouping; to investigate rotation, add independently specified angle conditions. An interval becomes useful when the reader can tell which source of variation it describes and how that source relates to the intended use of the model.

![Paired bootstrap distribution and actual error examples](https://ml-biomat.com/static/tutorials/machine-learning/figures/8ce6e8638c508014560cc958.svg?v=8ce6e8638c50)

Figure 3Upper left: 3,000 bootstrap draws of 450 original test images with their five positions, keeping fitted models fixed; solid line marks the mean difference and dashed lines the 95% percentile interval. Upper right: paired counts for right-shifted images. Bottom: first indexed image in each outcome group with true and predicted classes. There are no new augmentation errors in the right-shifted group; centered inputs do contain new errors. Digit attribution and CC BY 4.0 as in Figure 1.

Individual images matter as much as the statistical panel. Which translation errors did augmentation repair? Do the eleven remaining right-shifted errors contain similar strokes, or were some original digits already ambiguous? Inspect representative images, then organize the complete error group by true class, predicted class, and visible writing characteristics. The figure uses the first image by index from each outcome group, making the selection rule explicit. This kind of error analysis converts a vague wish for more accuracy into a testable next hypothesis, such as adding slant variation or examining the details that distinguish one frequently confused pair of digits.

## 6. Carry the experiment logic into six project families

**Tabular prediction: energy demand in the next interval.** Establish what information is available when a forecast is issued, such as previous demand, time, and an already released weather forecast. Use the preceding interval or the same time in the previous week as a baseline, then compare a linear model and boosted trees. Evaluate with rolling origins, using past observations at every issue time. If several buildings are available, hold out entire buildings to examine spatial transfer. Plot errors separately during low demand, peaks, and unusual weather, connecting improvements to a scheduling or alerting decision. Deliver the data dictionary, temporal split diagram, individual forecasts, and an explanation of how the prediction enters that decision.

**Object detection: locate items within a scene.** Begin with one class and a consistent annotation rule, including whether boxes cover visible parts or entire objects. Reproduce the smallest functioning training procedure for an open detector, then isolate one change, such as increased input resolution for small objects. Split by scene or video segment. Record AP under the same IoU convention, recall, and inference time. Show small objects, crowded regions, and occluded cases separately, including predicted boxes, confidence values, and missed regions. This lets a reader decide whether the intervention finds previously missed objects or mainly improves localization of objects already found. Save the evaluated predictions so that a later metric change can be investigated without retraining.

**Public-document question answering: connect answers to evidence.** Choose a fixed version of clearly licensed documents and build questions with supporting passages. Start with keyword retrieval, compare vector or hybrid retrieval, and then add the answer model. Retrieval recall measures whether evidence reached the context; answer evaluation checks factual claims and citation support. Record these stages separately. Hold out questions by source document or topic, and include questions whose answers are absent from the collection. An informative project figure links a question, retrieved passages, answer claims, and supporting passages. It reveals whether a failure originated in retrieval, context construction, or answer generation. The reproduction package should retain document versions and the retrieval settings that produced each answer.

**Audio recognition: listen under different recording conditions.** Choose environmental sound classification or speech transcription and fix the sample rate, segment duration, and label definitions. A spectral representation with a linear classifier provides an understandable baseline; a pretrained acoustic representation supplies a useful comparison. Split speech by speaker and environmental audio by recording source, keeping crops from the same recording together. Change noise level and recording device in controlled evaluations. Report aggregate performance and play representative mistakes alongside spectrograms. For transcription, examine word error rate, omitted words, and substitutions rather than relying on a single sentence score. The audible evidence helps explain what a representation retains and which disturbances interfere with the task.

**Spatiotemporal forecasting: predict where congestion will develop.** Represent locations as nodes and transport connections or spatial proximity as edges, then predict future flow at each location. Establish seasonal-naive and independent temporal baselines before introducing a graph model or cross-location attention. Temporal splits control future information; holding out locations studies transfer to unfamiliar places. Keep the forecast horizon and input window consistent across methods. Separate network-wide error, local peaks, and behavior under missing observations. A useful result links a map, observed and predicted time traces, and error versus forecast horizon. The map then explains a particular spatial pattern in the prediction rather than serving as decoration detached from the measured outcome.

**Games and control: choose actions that change future situations.** Start with an environment whose states and rewards can be inspected, such as grid navigation or a linear dynamical system. Compare random actions, a simple rule, or an existing controller with Q-learning, PPO, or another method appropriate to the action space. Specify the total number of environment interactions, use several training seeds, and evaluate on independent episodes. Record return distributions and replay successful and unsuccessful trajectories. If reward rises alongside unnecessary detours or repeated collisions, inspect the reward definition and action constraints. Deliver the environment version, policy, evaluation seeds, and trajectories so that another person can reproduce the behavior as well as the final scalar return.

These six directions can each produce a complete project. They share an explicit question, a trustworthy baseline, an isolatable intervention, a split that matches intended use, and examples that explain the outcome. The prerequisites depend on the object of study: [visual tasks](https://ml-biomat.com/tutorials/machine-learning/m13/en/) for detection, [RAG](https://ml-biomat.com/tutorials/machine-learning/m17/en/) for document questions, [audio](https://ml-biomat.com/tutorials/machine-learning/m20/en/) for sound, [time series](https://ml-biomat.com/tutorials/machine-learning/m21/en/) and [graph networks](https://ml-biomat.com/tutorials/machine-learning/m22/en/) for spatial forecasts, and [reinforcement learning](https://ml-biomat.com/tutorials/machine-learning/m24/en/) for control. The variety comes from the questions; the standard of evidence can remain consistent. Select the project whose observations and errors you are willing to examine closely.

## 7. Give figures, tables, and prose distinct jobs

An experimental paragraph can answer four questions in sequence: what was evaluated, what changed, how large the observed change was, and which figure explains its location. For this experiment: “On 450 held-out digit images evaluated at five positions, translation augmentation increased mean accuracy from 62.27% to 98.00%, while centered-image accuracy changed from 99.56% to 98.67%. Repeating each original image five times, with its total loss weight preserved, left predicted classes unchanged. The results connect the improvement under one-pixel translations to the additional position information.” The evaluated objects, control, and result appear together, giving the reader a direct route back to the figures and program.

The corresponding Chinese statement should preserve the same scope and numbers: “在450张留出数字及其五种位置上，平移增广将平均准确率由62.27%提高到98.00%；居中图像准确率由99.56%变为98.67%。保持原样本总损失权重后，五份相同复制没有改变类别预测。” Terms such as held-out and five positions identify the role of observations and the evaluation condition. Percentage points specifies a directly subtracted difference. Translating technical writing means preserving the experiment and its meaning, including conditions and units. A more dramatic adjective in one language would alter the claim even if all of the numerical values remained unchanged.

Figures make patterns visible, tables make values easy to retrieve, and prose explains relationships. A heat map compares combinations of model and position. A paired table retains who improved on the same observation. A bootstrap distribution shows sampling variation. An image contact sheet reveals the objects being counted. A useful caption identifies the data group, defines axes or colors, and states the important comparison conditions. If a truncated axis reveals a small difference, its range should be unmistakable. If panels use different color scales, the labels should make the difference visible. Readers should be able to understand a figure without reconstructing hidden conventions from the surrounding code.

A paper's central figure is often an effective entry point for reproduction. Rebuild the smallest dataset and calculation needed to produce it, checking coordinates, normalization, averaging, and the meaning of error bars. Then restore the broader setting step by step. Once a trend is reproduced, an additional condition can become an extension experiment. If the outcome differs, trace data preparation, the objective, parameters, and evaluation separately. This process creates specific material to write about: the phenomenon recovered, the setting that changed it, and the next experiment that distinguishes competing explanations. It also prevents the report from becoming a chronological account of software operations.

## 8. Hand the result to the next person who will run it

A reproducible result provides a route from input to figure. Here main.py is the common entry point, with the candidate parameters and seeds visible in the program. Tested dependencies, run instructions, and data attribution accompany the example archive. splits.json fixes observation membership; predictions.npz stores individual outputs; results.csv supplies material for a results table; summary.json records checkable calculations; SVG figures remain readable when enlarged. The data fingerprint helps verify that two runs processed the same pixel values and labels. Each file serves a concrete purpose in reconstructing a result, making the package easier to use and maintain.

A new reader can begin with a few small checks. The 450 test images and 1,347 development images must not overlap. All five positions must preserve each digit's total ink value. The four cells of the paired table must sum to 450. These checks protect observation membership, transformation meaning, and statistical counting respectively. Only then is it useful to compare the final scores. When a platform or library version changes, inspect these definitions first and then examine solver tolerance and floating-point differences. That order makes it easier to identify the cause of a discrepancy than immediately pursuing the last decimal place.

The next investigation might extend one-pixel translation to rotation, new writers, or different imaging devices. For each new condition, explain why labels are preserved, identify the sampling unit, and expose the existing baseline to the same evaluation inputs. This gives each additional experiment a clear place in the research question. Code becomes a reusable experimental instrument, images become evidence that can be discussed, and prose connects the question to the observation. A completed course project then has the structure needed for continued research: explicit definitions, inspectable comparisons, and a practical way to add new evidence.

[Download complete code and data](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M28.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Improving Reproducibility in Machine Learning Research](https://jmlr.org/papers/v22/20-303.html)

   History of the reproducibility program and the connection between code and experimental conditions.

   Public technical reference; explanatory text and experiment independently written.
2. [Dive into Deep Learning — Image Augmentation](https://d2l.ai/chapter_computer-vision/image-augmentation.html)

   Learning from transformed images; the controlled SVM experiment here is independently implemented.

   Public technical reference; explanatory text and experiment independently written.
3. [Optical Recognition of Handwritten Digits](https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits)

   Data semantics, original writer split, and CC BY 4.0 license.

   Data CC BY 4.0; original digit attribution retained.
4. [scikit-learn — load_digits](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_digits.html)

   The bundled 1,797 digits and pixel range.

   Public technical reference; explanatory text and experiment independently written.
5. [scikit-learn — Support Vector Machines](https://scikit-learn.org/stable/modules/svm.html)

   SVC objective, C, and kernel-classification implementation.

   Public technical reference; explanatory text and experiment independently written.
6. [scikit-learn — Common Pitfalls](https://scikit-learn.org/stable/common_pitfalls.html)

   Operational treatment of splits, leakage, and randomness.

   Public technical reference; explanatory text and experiment independently written.
7. [NeurIPS Paper Checklist](https://neurips.cc/public/guides/PaperChecklist)

   Organizing experimental settings, reproducibility material, and claims.

   Public technical reference; explanatory text and experiment independently written.
