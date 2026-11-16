# 综合项目：把一个改进写成可以复现的证据

Source: https://ml-biomat.com/tutorials/machine-learning/m28/
Language: zh-CN

同一张数字挪动一格，准确率为什么骤降？用完整增广对照串起复现、消融、统计与实验写作。

## 1. 一个几乎满分的识别器，为什么经不起挪动一格

把邮政编码写在方格中央，识别器几乎每次都答对；把同样的数字向右挪一点，它却认错了将近一半。数字没有变，墨迹也没有丢，改变的只是位置。这个小现象很适合成为一个研究项目的起点：模型学会了数字的形状，还是过分依赖笔画出现的固定位置？接下来应该增加网络深度、加入位置变化的训练样本，还是先检查测试过程？一个有价值的项目从可以观察的差别开始，再把这些可能的解释逐一分开。

本章用真实的公开手写数字做完整实验。基线在居中的450张测试图上识别正确448张，准确率为99.56%；把中心、左、右、上、下五种位置等权计入评价，平均准确率降到62.27%。加入位置增广后，五位置平均达到98.00%，居中准确率则为98.67%。这组结果同时包含很大的改进与一个较小的代价。我们要解释改进从哪里来、对什么图像成立，以及怎样把程序、数字和文字连成别人能够检查的证据。

机器学习的复现实践也围绕这种问题发展。Pineau等人在2021年的报告中回顾了NeurIPS 2019复现计划：公开代码、组织复现挑战和记录实验条件被放在同一项工作中。代码解决“怎样计算”，数据与设置决定“计算的是什么问题”。在阅读一篇论文时，可以先选一项明确主张，例如“某种增广提高了位置变化下的识别”，找到支撑它的实验图，再追到训练划分、变换和指标定义。这样读论文，公式、程序和结论就有了共同的对象。

这里延续《动手学深度学习》中通过图像变换扩展训练经验的思想，用核SVM做一个体量较小、容易控制变量的实验。它检验的是位置增广的机制，采用本章明确给出的数据划分和设置。先把一个方法思想落实成可计算的假设，随后再讨论怎样复现原论文的特定结果，两类工作都能产生有用的知识。关键是让题目和实验回答同一个问题。

## 2. 在训练之前，先认清一条样本是什么

实验使用scikit-learn内置的1797张8×8数字图像，标签为0至9。原始像素值在0至16之间，可以理解为归一化字形中一个小区域的墨迹计数；除以16后，输入落在0至1。每张图放入10×10的零背景画布，四周留出一圈空白。平移一个像素时，这圈空白接住边缘笔画，因此变换不会裁掉墨迹。看似普通的边界处理实际上保护了实验假设：改变位置的同时，尽量保持被识别的形状。

![同一数字的受控位置变化](https://ml-biomat.com/static/tutorials/machine-learning/figures/51663b8058a958d51c3eb4b8.svg?v=51663b8058a9)

图 1同一原始字形放在10×10画布的五个位置；图中展示三个真实测试样本，灰度0–1，边框留白使一像素平移保留全部墨迹。数据：Alpaydin与Kaynak，UCI Optical Recognition of Handwritten Digits，CC BY 4.0；本图为原始数据的变换展示。

数据来自Alpaydin与Kaynak的UCI手写数字数据集，公开页面采用CC BY 4.0许可。原始数据组织曾按书写者划分训练与测试，scikit-learn提供的是其中的1797张图像。本章在这批图像内部重新按类别比例划分450张测试图和1347张开发图，因此结果描述的是这批图像上的留出评价。若项目目标是识别从未见过的人的笔迹，应取得书写者标识，并按人划分；同一个人的十张字形不能被当作十个完全不同的使用者。

再从开发集抽出270张作验证，剩余1077张用于选参数时训练。先划分原始图像，再分别生成它们的五种位置。这样，同一张图的中心版本与右移版本始终属于同一侧。如果先增广再随机拆分，训练集可能见过某张图的左移版本，测试集却拿它的右移版本考模型；这时评价更接近“认出同一个样本的另一张照片”。采样单位决定了我们能对什么对象推广，划分操作必须服从这个单位。

一份简洁的数据卡应把这些约定留下来：一行表示一张原始图像，标签如何取得，像素范围是什么，哪些样本进入哪一组，变换是否改变标签，以及使用者可以怎样获取和使用数据。对于声音，采样单位可能是说话者或录音；对于需求预测，可能是日期与地点；对于文档问答，则可能是一份文档及其多个问题。数据卡并不需要写成冗长说明，它要让接手的人立即知道每一行数据与真实世界的关系。

## 3. 增广有效，是因为看到了新位置，还是因为样本数变多了

我们安排三组训练条件。第一组只用居中图像；第二组把每张居中图像原样复制五份；第三组用中心及四个方向各移动一格的五种图像。第二组是一个很有用的对照：它与第三组拥有同样多的训练行，却没有新位置的信息。三组共享同一开发集、同一测试集、同一种RBF核与同一参数候选表。这样，观察第三组的变化时，就可以把“增加了行数”与“增加了位置变化”分开讨论。

还有一个容易藏在实现里的变量。SVM的软间隔目标包含所有训练样本损失的总和，直接复制五份会让损失项扩大五倍，相当于改变了正则化与拟合误差的平衡。为了保留每张原始图像的总权重，复制或增广五份时，把传给SVC的C除以5。每一份的权重变小，五份合起来仍然对应原来的一张。对多类别SVC，二分类子问题采用相同规则；这个控制关注的是学习目标中的权重，而不只是文件里有多少行。

$$
J_k(w)=\tfrac12\|w\|^2+\frac{C_0}{k}\sum_{i=1}^{n}\sum_{j=1}^{k}\ell_{ij}(w),\qquad \ell_{ij}=\max(0,1-y_i f_w(x_{ij}))
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/acdad4257c29c3f9dad2a348.svg) | 核特征空间中的权重与含偏置的二分类决策函数；本例输入和得分无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/19ba377343847499549adf7a.svg) | 原始训练图像数、每图视图数、原图索引与视图索引；计数，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/31fd8bf45874cdf65e568268.svg) | 第i张图的第j种视图及二分类子问题的±1标签；100维像素输入归一到0–1。 |
| ![Formula](https://ml-biomat.com/static/agent-math/fa309d8becb78768250709af.svg) | 基础损失权重、hinge损失与目标值，均按无量纲数值计算；SVC实际C=C0/k。 |
| ![Formula](https://ml-biomat.com/static/agent-math/17e4be483413f8a681b9b712.svg) | 权重向量的平方范数；核方法在核特征空间衡量这个量。 |

若一张图的损失为0.4，C0=10，则原样本贡献10×0.4=4。复制五份并使用C=2，贡献为2×5×0.4=4；若仍用C=10，贡献会变为20。增广时五种视图的损失通常不同，C0/k保留每原图的总权重，并让模型学习这五种输入。多类别SVC通过二分类子问题组合类别决定。

核宽度固定为gamma=0.05，基础C只在1、3、10三个值中选择。每组都用验证集五位置平均准确率选择C，分数相同则保留较小值。选完之后，用全部1347张开发图重新拟合，再对预留的450张测试图进行评价。实验使用11、29、47三个内层划分种子，改变哪些开发图负责验证。测试集始终固定，直到所有规则确定以后才用于结果比较。超参数选择已经属于方法的一部分，所以基线也应得到同等的选择机会。

比较预算时要区分“尝试次数相同”与“计算量相同”。这里每组都尝试三个C，但增广组的核矩阵更大，训练代价也更高。若研究目标是固定算力下谁更好，就应给出共同时间预算，并在这个预算内选择设置；若研究目标是查清位置变化是否提供有效信息，则先保持模型与每原样本的损失权重一致。公平的比较来自明确的问题，不是把所有配置强行设成一样。

## 4. 运行完整实验，再读一张有比较条件的图

下面的脚本完成数据划分、三组参数选择、开发集重拟合、逐样本预测、成对统计和作图。数据随scikit-learn提供，运行时不需要额外下载。输出中的splits.json记录每个原始图像的编号，results.csv保存各组的验证与测试结果，predictions.npz保留逐图、逐位置的预测。读取这些文件，就能从图表上的一个数字回到它所汇总的具体样本，而不必重新猜测当时的划分。

### 完整实验：三组对照、逐样本预测与成对bootstrap

脚本直接生成数据划分、结果表、统计摘要和三组图。固定测试划分2801、内层选择种子11/29/47、bootstrap种子2802。

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

左侧热图把五种位置分别展示。基线在中心位置接近满分，向下移动时只有46.44%；增广组在五种位置上都接近97%至99%。这说明总体平均值的提高主要发生在发生平移的输入上，居中输入还出现了少量新错误。中间与右侧的点图分别保留这两种评价目标；把所有图像混成一个准确率，会掩盖“位置更稳健、中心略有下降”这件具体的事。

![三组训练条件与不同位置的识别结果](https://ml-biomat.com/static/tutorials/machine-learning/figures/94bb9aa3d3d7d8410d13a5e2.svg?v=94bb9aa3d3d7)

图 2左：选择划分11后，固定450张测试图的各位置正确率；格中数值为%。中与右：三个内层选择种子对应的中心及五位置平均准确率，细线连接同一种子的三组。三个种子均选C0=10，在同一开发集重拟合后预测相同，点的位置略作水平错开便于辨认；未将重合点当作独立试验误差条。

复制组与原样本组在全部测试位置上的类别预测完全一致。配合C除以5的权重控制，它支持我们把主要变化归到位置信息上。增广组比基线的五位置平均准确率高35.73个百分点，而不是“提高35.73%”：前者直接相减，后者通常表示相对基线的比例。只要把单位写清楚，读者就不需要猜测作者采用了哪一种算法。支持向量条目的数量则从486、1119到2876有所变化；复制样本会改变条目的组织，这个数也要结合数据表示来理解。

三个选择种子的最终测试点为什么重合？它们都选中了基础C=10，随后又在同一1347张开发图上训练同一个确定性的SVM，所以最终模型的类别预测相同。种子在这里控制的是内层划分，并没有自动制造三个独立的测试实验。这个观察尤其值得保留：写了多个种子，还需要说明它们究竟改变了什么。若要研究训练初始化的不确定性，应选择含随机初始化的模型；若要研究样本选择的变化，应设计不同的外层划分。

## 5. 把两种模型放在同一张答卷上比较

分别给两种模型计算一个平均分，会丢掉它们在同一张图上怎样变化的信息。对450张右移测试图，基线与增广模型共同答对229张，增广额外答对210张，二者共同答错11张，基线单独答对的为0张。把这些数量放入一个2×2表，改进来自哪些样本就清楚了。共同答对与共同答错的部分会在差值里抵消，真正改变差值的是两组意见不一致的样本。

$$
n=n_{11}+n_{10}+n_{01}+n_{00},\quad a_A=\frac{n_{11}+n_{10}}n,\quad a_B=\frac{n_{11}+n_{01}}n,\quad \Delta=a_B-a_A=\frac{n_{01}-n_{10}}n
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/f12c13576bb625453e573142.svg) | 在相同观测上比较的基线与增广模型。 |
| ![Formula](https://ml-biomat.com/static/agent-math/aeeca924111fd3a75173acfe.svg) | 第一位a表示A是否正确，第二位b表示B是否正确，1正确、0错误；nab为相应样本数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f524fa4611e4410e9a58920a.svg) | 样本总数、两模型正确率与正确率之差；要求n>0，正确率无量纲，100Δ以百分点表示。 |

若共同正确6张、仅A正确1张、仅B正确3张、共同错误0张，总数10。A=7/10，B=9/10，差为(3−1)/10=0.2，即20个百分点。两者共同正确的6张在相减时抵消；两组不一致的样本决定差值。

### 交互：把改进拆成两组分歧

四格记录同一批样本上两模型是否答对。调整计数，观察正确率与差值如何联动；先试十张图的小例子，再回到右移实验。

[Figure: 成对计数矩阵与正确率](https://ml-biomat.com/tutorials/machine-learning/m28/#M28-plot)

每个计数以样本为单位；两个模型始终面对同一批样本。增广单独正确会增大差值，基线单独正确会减小差值。

完整实验还要同时考虑五个位置。先对每张原始图像求两种模型的五位置平均正确率，再相减，得到450个成对差值。重新抽样时，一次抽走的是一张原始图像及其五个位置，而不是把2250个位置图像当成彼此独立的观测。这样保留了同一字形几个版本之间的关联。脚本以原图为单位有放回抽样3000次，每次都重新计算平均差值，用这些结果观察有限测试样本带来的波动。

$$
d_i=\frac1K\sum_{j=1}^{K}\left[\mathbf1(\widehat y^{B}_{ij}=y_i)-\mathbf1(\widehat y^{A}_{ij}=y_i)\right],\quad\bar d=\frac1n\sum_{i=1}^{n}d_i,\quad\bar d^{*(b)}=\frac1n\sum_{r=1}^{n}d_{I_{br}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/70e731e73bce482ecf0af045.svg) | 原始测试图像数、每图位置数、原图与位置索引；本例n=450、K=5。 |
| ![Formula](https://ml-biomat.com/static/agent-math/811d7e06c9188f193ccfb450.svg) | 真实类别、模型A/B对位置j的预测与指示函数；条件成立返回1，否则0，均无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/01b6557f1746d01716e2e7a4.svg) | 每原图的五位置平均差、所有原图平均差与第b次bootstrap平均差；均为正确率差，乘100为百分点。 |
| ![Formula](https://ml-biomat.com/static/agent-math/47b2a5dc5ab32f0013c327f0.svg) | bootstrap轮次、该轮抽样位置、从1到n等概率有放回抽到的原图索引；同图所有位置一起抽取。 |

两张图的差值分别0.2、0.6，原均值0.4。每次抽两张，有放回可能得到索引(1,1)、(1,2)、(2,1)、(2,2)，对应均值0.2、0.4、0.4、0.6。真实实验抽3000轮，取均值分布2.5%与97.5%分位数形成95%百分位区间；抽样单位保持为原图。

这次成对bootstrap的95%百分位区间为33.73至37.69个百分点，中心估计为35.73个百分点。区间描述的是固定模型与当前采样单位下，测试图像重采样产生的差值变化；它没有把另一个书写者群体、任意旋转或重新训练的变化混进来。若下一步关心新的书写者，就把书写者作为新的分组单位收集和评价；若关心旋转，就增加独立的角度条件。统计区间的含义跟随抽样过程，每一种变化都应有自己的实验位置。

![成对重采样区间与真实字形错误](https://ml-biomat.com/static/tutorials/machine-learning/figures/3b31dda8d0a14384c2fce675.svg?v=3b31dda8d0a1)

图 3上左：固定模型下，以450张原始测试图为单位、携带各自五种位置的3000次bootstrap，实线为平均差，虚线为95%百分位区间。上右：450张右移图的成对计数。下：各结果组按索引选择第一张，标出真值及两模型预测；“增广新错”组在右移条件下为0张，中心条件仍有新增错误。数据字形按CC BY 4.0署名同图1。

下面的具体字形与统计图同样重要。增广修复了哪些偏移造成的错误？剩下的11张右移图是否具有相似笔画，还是原图本身就难以区分？先查看程序选出的代表，再把整个错误组按真实类别、预测类别与字形特征整理。这里展示的是每组按索引选出的第一张，选择规则固定。这样的误差分析会把“再提高一点准确率”变成可执行的假设，例如增加倾斜变化，或检查某一对易混数字的细节。

## 6. 把同一套实验逻辑带到六类综合项目

**表格预测：下一时段的能耗。**先确定预测发出时已经知道哪些信息，例如过去的用量、时刻和已发布的天气预报。用上一时段或同一星期的用量作为基线，再比较线性模型与提升树。按时间滚动评价，在每个预测起点只使用过去数据；若有多个建筑，还可保留整栋建筑检验空间迁移。最后按低负荷、高峰和异常天气分别画误差，解释模型改善了哪个工作环节。项目交付包括数据字典、时间切分图、逐时段预测和一个明确的调度或预警用途。

**图像检测：找出画面中的对象。**从一个类别和稳定标注规则开始，确定边界框包住可见部分还是完整对象。复现一个开放检测器的最小训练流程，再选一个改动，例如增加小目标图像的输入分辨率。以拍摄场景或视频片段划分数据，记录同一IoU规则下的AP、召回率和推理时间。把小目标、密集对象与遮挡样本分别展示，检测框、置信度和漏检区域同时出现。这样可以判断改动究竟减少了漏检，还是只让已经找出的框更贴近边缘。

**公开文档问答：让答案能找到依据。**选取许可明确、版本固定的公开文档，围绕实际使用者的问题建立一组问答与证据段落。先做关键词检索，再比较向量检索或混合检索，最后接入回答模型。检索召回率检查证据有没有进入上下文，答案评价检查事实与引用是否一致，两层分别记录。按文档来源或主题留出测试问题，加入文档中没有答案的提问。项目的核心图可以把问题、召回片段、答案中的主张与支持段落连起来，直接显示错误发生在哪一环。

**音频识别：在不同录制条件下听清声音。**先选择环境声音分类或语音转写，并固定采样率、片段长度及标签定义。以频谱特征配线性分类器作为容易理解的起点，再比较预训练声学表示。语音任务按说话者划分，环境声音按录音来源划分，避免同一录音裁出的片段出现在两侧。逐项改变噪声强度与录制设备，既报告总体分数，也播放有代表性的错误片段；语音转写同时观察词错误率、漏词与同音替换。听觉证据与频谱图一起帮助解释模型的选择。

**时空预测：下一小时哪里更拥挤。**把地点作为节点、交通联系或空间距离作为边，预测一组地点的未来流量。先用季节朴素预测和逐点时间模型建立基线，再加入图模型或跨地点注意力。时间切分控制未来信息，保留部分地点则考察新地点上的迁移。比较时同时固定预测步长与输入窗口，并区分全网误差、个别高峰和缺测恢复。一个有用的结果展示应让地图、真实与预测时间曲线、误差随预测步长的变化彼此对应，而不只是给出一张彩色网络图。

**游戏与控制：动作怎样改变后续处境。**从状态和奖励都能检查的小环境开始，例如网格导航或线性摆动系统。用随机策略、简单规则或已有控制器作参照，再实现Q-learning、PPO或适合该动作空间的方法。明确环境交互总步数，在多个训练种子与独立评价回合上记录回报分布，同时回放成功和失败轨迹。若奖励增加，却伴随不必要的绕路或频繁碰撞，就回到奖励定义与动作约束检查。交付时保存环境版本、策略、评价种子和轨迹，让他人能重新看到策略怎样行动。

六类项目可以各自形成完整作品，也可以共享同一套组织方法：一个明确问题、一个值得信任的基线、一项可以隔离的改动、与使用方式一致的划分，以及能解释结果的样本。先修模块随对象变化：检测接到[视觉任务](https://ml-biomat.com/tutorials/machine-learning/m13/)，文档问答接到[RAG](https://ml-biomat.com/tutorials/machine-learning/m17/)，声音接到[音频](https://ml-biomat.com/tutorials/machine-learning/m20/)，时空任务接到[时间序列](https://ml-biomat.com/tutorials/machine-learning/m21/)与[图网络](https://ml-biomat.com/tutorials/machine-learning/m22/)，控制接到[强化学习](https://ml-biomat.com/tutorials/machine-learning/m24/)。选题的丰富性来自问题本身，完成标准则可以保持一致。

## 7. 让图、表和文字各自完成一件事

写实验段落时，可以依次回答四件事：评价对象是什么，改变了什么，观察到多少变化，以及哪一幅图解释变化发生在哪里。例如本章可以写：“在450张留出数字及其五种位置上，平移增广将平均准确率由62.27%提高到98.00%；居中图像准确率由99.56%变为98.67%。保持原样本总损失权重后，五份相同复制没有改变类别预测。结果显示，新增位置信息改善了模型对一像素平移的识别。”对象、比较条件与结果就在同一段里，读者可以据此返回图和程序。

英文表达保持相同的对象与数值：“On 450 held-out digit images evaluated at five positions, translation augmentation increased mean accuracy from 62.27% to 98.00%, while centered-image accuracy changed from 99.56% to 98.67%. Repeating each original image five times, with its total loss weight preserved, left predicted classes unchanged.”这里的held-out说明样本用途，five positions说明评价条件，percentage points适合在随后报告直接相减的差值。译文应该传递相同实验，而不是给中文结论增加新的强度。

图负责让规律可见，表负责让数字容易查，正文负责解释关系。热图适合比较模型与位置的组合；成对表保留同一张图上谁改对了；bootstrap分布表达抽样变化；字形接触表让读者看见被统计的对象。每幅图的图注至少交代数据来自哪一组、横纵轴或颜色表示什么，以及比较时保持了哪些条件。若采用截断纵轴来展示很小的差异，应让刻度和范围清楚可见；若多组使用不同色标，读者就需要在图上得到明确提示。

论文中的一幅关键图往往是最好的复现入口。先重建生成它所需的最小数据和计算，核对坐标、归一化、平均方式及误差条含义，再逐步恢复完整设置。得到相近趋势后，可以增加一项新条件形成扩展实验；若结果不同，就沿数据处理、目标函数、参数和评价逐层定位。这样形成的文字有具体对象可写：恢复了哪一个现象，哪一个设置改变了结果，下一项实验要区分哪两个解释。

## 8. 把成果交给下一个愿意运行它的人

一个可复现成果应能从输入一路走到图表。本章的main.py是统一入口，固定的参数候选表和种子在代码中可见；依赖版本、运行方法与数据许可随示例包保留。splits.json把数据划分固定到索引，predictions.npz保存逐样本结果，results.csv提供论文表格的原料，summary.json记录可核对的计算，SVG图可以直接用于讲解。数据指纹则帮助检查两次运行究竟读取了同一批数字与像素值。

接手者可以先运行一个小检查：450张测试图与1347张开发图没有重叠，五种位置保持每张图的总墨迹量，成对表的四格之和等于450。然后才比较完整结果。这些检查分别守住数据归属、变换含义和统计计数，任何一项失配都会改变实验的问题。遇到平台与库版本变化时，先检查这些定义，再检查优化器容差与浮点差异，比直接追逐最后几位小数更容易找到原因。

从这里继续研究，可以把一像素平移扩展为角度变化、不同书写者或不同成像设备。每次新增一种变化，都先说清标签为什么保持、采样单位是什么，以及已有基线要怎样面对同样的输入。这样，代码成为可延续的实验工具，图像成为可以讨论的证据，文字则把问题与观察接起来。一个完成的课程项目，也就具备了继续生长成研究工作的结构。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M28.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Improving Reproducibility in Machine Learning Research](https://jmlr.org/papers/v22/20-303.html)

   复现计划的历史与代码、实验条件之间的联系。

   Public technical reference; explanatory text and experiment independently written.
2. [Dive into Deep Learning — Image Augmentation](https://d2l.ai/chapter_computer-vision/image-augmentation.html)

   用变换扩展训练经验；本章独立编写受控SVM实验。

   Public technical reference; explanatory text and experiment independently written.
3. [Optical Recognition of Handwritten Digits](https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits)

   数据语义、书写者划分与CC BY 4.0许可。

   Data CC BY 4.0; original digit attribution retained.
4. [scikit-learn — load_digits](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_digits.html)

   内置1797张数字与像素范围。

   Public technical reference; explanatory text and experiment independently written.
5. [scikit-learn — Support Vector Machines](https://scikit-learn.org/stable/modules/svm.html)

   SVC目标、C与核分类实现。

   Public technical reference; explanatory text and experiment independently written.
6. [scikit-learn — Common Pitfalls](https://scikit-learn.org/stable/common_pitfalls.html)

   划分、泄漏与随机性的操作约定。

   Public technical reference; explanatory text and experiment independently written.
7. [NeurIPS Paper Checklist](https://neurips.cc/public/guides/PaperChecklist)

   实验条件、复现材料与主张的组织。

   Public technical reference; explanatory text and experiment independently written.
