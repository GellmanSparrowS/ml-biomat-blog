# Images as computable structure: convolution, residuals, and transfer

Source: https://ml-biomat.com/tutorials/machine-learning/m12/en/
Language: en

Start with nine products, then use real handwriting to inspect recognition, errors, and adaptation.

## Can a digit move without changing its identity?

Write an “8” on paper, then move the paper slightly to the right. Most people still recognize the digit. For a computer, that motion changes the positions of many pixel values. Flattening an image into one long vector and feeding it to a fully connected network assigns separate weights to different positions. The same short stroke in the upper left and lower right may need to be learned separately. A convolutional network starts from spatial structure and builds in the idea that a useful local pattern may recur at different locations.

Real handwritten images connect three questions in this chapter: how does a small kernel turn pixels into local features, how do those features support an image-level classification, and how can learned features transfer to new classes? Alongside a small CNN, we test images shifted right by one pixel. We also pretrain on digits 0–4, then use a small set of digits 5–9 to compare frozen features, fine-tuning, and training from scratch. Image processing, evaluation, and transfer become parts of one runnable investigation.

A grayscale image is a two-dimensional table whose entries measure brightness or intensity at spatial positions. An RGB image supplies three such measurements per position: red, green, and blue. These channels describe the same spatial locations rather than three unrelated photographs. Camera data also involve exposure, encoding, and color spaces. Our input is simpler: each image contains 8×8 integers between 0 and 16, obtained by counting active pixels in blocks of an original handwritten bitmap. Dividing by 16 gives dimensionless inputs between zero and one.

## A small template reads the whole image

Place a 3×3 template containing nine weights over a small image region. Multiply each pixel by the corresponding weight, then add the nine products to obtain one response. Move the template and repeat. Scanning the image produces another table, called a feature map. The same nine weights are reused at every position: this is parameter sharing. During training, contributions from different positions accumulate into the gradient of the same weight, allowing one template to adapt to patterns encountered throughout the images.

$$
Y_{o,r,s}=b_o+\sum_{c=1}^{C_{\mathrm{in}}}\sum_{u=0}^{k_h-1}\sum_{v=0}^{k_w-1}K_{o,c,u,v}\,X_{c,r+u,s+v}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/871a117fa007ef6935e35aae.svg) | Input tensor: channels × height × width; intensities are dimensionless after division by 16. |
| ![Formula](https://ml-biomat.com/static/agent-math/14682edf48bc589a68dff1f5.svg) | Learned kernel weights, indexed by output channel, input channel, and two spatial dimensions. |
| ![Formula](https://ml-biomat.com/static/agent-math/4def0809683bf7be8e0840a2.svg) | Output response for channel o, row r, column s, and its channel bias; dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/3ec52b56ebfaa3600a766fc6.svg) | Input-channel index and kernel row and column indices. |
| ![Formula](https://ml-biomat.com/static/agent-math/39dd0476c806711eec2d3db1.svg) | Input/output channel counts, kernel height/width, and input height/width; all counts. |

This form uses stride one, no padding, and cross-correlation without flipping the kernel. For a single-channel patch with rows (0,0,1), kernel rows (−1,0,1), and zero bias, each row contributes one and the response is three. Multiple input channels add their contributions. Kernel weights are shared across different r and s positions.

For a hand calculation, let every template row be (−1, 0, 1), and every row of the covered image patch be (0, 0, 1). Each row contributes −1×0 + 0×0 + 1×1 = 1, so the total response is 3. The template responds positively to a vertical dark-to-light boundary. Reversing the boundary makes the response negative; covering a uniform region produces zero because positive and negative weights cancel. The kernel acts like a small instrument measuring local change, with every contribution available for inspection.

Deep-learning libraries commonly call the operation convolution even when the kernel is not flipped. More precisely, this convention is cross-correlation, and our formula follows PyTorch. Learned kernels have no prescribed orientation labels, so the convention is compatible with training; hand calculations still need to match the library. With multiple input channels, an output channel reads a kernel-shaped patch from every input channel, sums their contributions, and adds a bias. Different output channels use different weights and can respond to different local patterns.

$$
P=C_{\mathrm{out}}\bigl(C_{\mathrm{in}}k_hk_w+1\bigr)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/1aaddf0d4be4d873ff6c0600.svg) | Parameter count of an ordinary convolutional layer with bias, an integer. |
| ![Formula](https://ml-biomat.com/static/agent-math/6e8ea1ef1c2843b67d533a09.svg) | Input and output channel counts; this formula assumes no grouped convolution. |
| ![Formula](https://ml-biomat.com/static/agent-math/b75fe22b20830182aee39fbd.svg) | Kernel height and width, counted in pixel positions. |
| ![Formula](https://ml-biomat.com/static/agent-math/95836ae470c61ab15bfb67d6.svg) | One additional bias parameter per output channel. |

Each output channel needs C_in spatial kernels and one bias. The first 1→8, 3×3 layer has 80 parameters; the 8→16 layer has 1,168; the 64→10 head has 650, giving 1,898 total. Image dimensions affect how many positions are processed but do not directly enter this shared-parameter count.

One input channel and eight 3×3 output kernels with biases require 8×(1×3×3 + 1) = 80 parameters. Enlarging the input from 8×8 to 80×80 leaves this parameter count unchanged, although the operation must run at more spatial positions. Sharing therefore turns an assumption about repeated local rules into a concrete computational structure. Images, time–frequency maps, and regularly sampled fields all provide grid neighborhoods in which such an assumption can be useful.

## Boundaries, strides, and a growing field of view

Near an image edge, part of a sliding template would fall outside the observed grid. Valid convolution retains only positions where the full template lies inside, making the output smaller. Padding supplies extra values around the boundary so the template can be evaluated around original edge positions too. Zero padding assigns zero outside the image; reflection padding mirrors nearby values. These choices encode different assumptions about the boundary. For measured images or physical fields, the assumption should match the meaning of the data as closely as the task requires.

$$
n_{\mathrm{out}}=\left\lfloor\frac{n+2p-k}{S}\right\rfloor+1,\qquad r_\ell=r_{\ell-1}+(k_\ell-1)j_{\ell-1},\quad j_\ell=S_\ell j_{\ell-1}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/081412c66cbf83929b8e1b9c.svg) | Input and output lengths along one spatial direction, counted in grid positions. |
| ![Formula](https://ml-biomat.com/static/agent-math/4ae3f422930e98f3a99ecff2.svg) | Padding per side, kernel width, and positive integer stride; dilation is one here. |
| ![Formula](https://ml-biomat.com/static/agent-math/e324cf06f94b000228b474a7.svg) | Floor operation, retaining fully evaluable positions. |
| ![Formula](https://ml-biomat.com/static/agent-math/09151dc95553bb8667adfd37.svg) | Layer index and that layer’s kernel width and stride. |
| ![Formula](https://ml-biomat.com/static/agent-math/9c233bd6c4b9d9308fa08b8a.svg) | Receptive-field width and spacing of neighboring feature locations in input-pixel units. |
| ![Formula](https://ml-biomat.com/static/agent-math/ebb617a8dcc5fd9713b9310d.svg) | Initial width and spacing at the input; nominal receptive fields can include padding. |

Apply the length expression separately to height and width. For n=8,p=1,k=3,S=2, floor(7/2)+1 gives four. Receptive width grows by (k−1) previous-layer spacings: a 3×3 convolution gives r=3,j=1; 2×2 stride-two pooling gives r=4,j=2; another convolution gives r=8; another pooling gives r=10,j=4.

Stride determines how many pixels the template moves at a time. An 8×8 image, 3×3 kernel, stride one, and one-pixel padding on all sides produce an 8×8 output. Changing stride to two produces 4×4. Pooling is another local operation. Max pooling retains the largest response in a window; average pooling computes its mean. A 2×2 patch containing 1, 3, 2, and 4 yields 4 under max pooling and 2.5 under average pooling. Neither learns kernel weights, but both affect spatial resolution and which details remain available downstream.

The receptive field of a deep feature is the input region on which that position can depend. A first 3×3 convolution sees a 3×3 region. A second stride-one 3×3 convolution expands it to 5×5. Downsampling increases the spacing between later feature positions in the original coordinates, causing subsequent layers to expand their receptive fields faster. Our convolution–pooling–convolution–pooling sequence has nominal widths 3, 4, 8, and 10 pixels. The final width includes padded positions, while the observed input is only eight pixels wide. Architectural coverage and actual observed content are therefore different quantities.

Under ideal conditions, sharing a template allows the feature map to move along with a translated input. This is translation equivariance. Keeping the final image label unchanged after translation is translation invariance. Boundaries, pooling, and stride affect the relationship between the two. Convolution supplies a useful structural starting point, while the complete classifier can remain sensitive to location and cropping. Our measured shift experiment will make that distinction visible in its predictions.

## Calculate a feature map, one patch at a time

The 7×7 input starts with ones on the right and zeros on the left. Click pixels to edit them. Kernel, stride, and padding changes recompute the output. The orange outline identifies the input patch for the selected output; nine products are added below. Pixel and output cells support keyboard focus and Enter or Space.

[Figure: Editable input, kernel, and output](https://ml-biomat.com/tutorials/machine-learning/m12/en/#M12-plot)

Rows and columns start at zero; positions outside the input are zero. Output color indicates sign and magnitude, with exact values written in the cells. Every local-mean kernel weight is 1/9.

## From local strokes to deeper networks

A CNN combines convolutions, nonlinear activations, and successive processing of local responses. Shallow layers access small neighborhoods; deeper layers combine information over wider regions. This organization supports complex image relationships with a manageable parameter count. Early LeNet systems brought local connectivity, shared weights, and downsampling together for end-to-end handwritten recognition. Modern document reading and microscopy tasks differ in scale and content, but the same local-to-global computational idea remains a useful starting point.

Increasing depth also makes optimization more demanding. The residual-network work released by He and colleagues in 2015 reformulated a block as a learned correction added to its input. If a block need not alter the representation, a residual branch near zero preserves it. A direct path also supplies another route for information and derivatives, supporting the construction of deeper networks. Related connections later appeared in Transformers and graph networks because they address information transfer across repeated transformations rather than a property unique to photographs.

$$
z=x+F(x;\theta),\qquad y=\operatorname{ReLU}(z)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/d52903f55ffbb1e8eaaa0191.svg) | Input, summed tensor, and activated output, with matching shapes; dimensionless here. |
| ![Formula](https://ml-biomat.com/static/agent-math/2e7656feccc67098b1dc854a.svg) | Residual branch parameterized by θ, producing a correction added to the input. |
| ![Formula](https://ml-biomat.com/static/agent-math/f1869de26e07bd8042e214a7.svg) | Elementwise activation retaining positive values and replacing negative ones with zero. |

For x=(0.8,0.4) and residual (−0.2,0.1), the sum is (0.6,0.5), unchanged by ReLU. A zero residual preserves a nonnegative input; negative values are altered by the final ReLU. If branch shapes differ, project the shortcut to a matching shape before coordinatewise addition.

![Computation through a residual block: the upper branch learns a correction and the lower branch carries the input directly, followed by addition and ReLU. The numerical example uses nonnegative input; the blue direct path and orange correction combine in the output. Original diagram from the computational definition.](https://ml-biomat.com/static/tutorials/machine-learning/figures/34c405c1c783ae0016d6c4a8.svg?v=34c405c1c783)

Figure 1Computation through a residual block: the upper branch learns a correction and the lower branch carries the input directly, followed by addition and ReLU. The numerical example uses nonnegative input; the blue direct path and orange correction combine in the output. Original diagram from the computational definition.

Adding two branches requires matching shapes. When spatial dimensions or channel count change, a 1×1 convolution with a suitable stride can project the shortcut into the required shape; that projection has learned parameters. An activation after addition also affects the exact conditions for an identity mapping. Our code sets a residual convolution’s weights and bias to zero, applies addition followed by ReLU to nonnegative inputs, and verifies a maximum input–output difference of zero. This isolates one structural property, while the full classification experiment trains a small network with two convolutional layers.

The small classifier transforms an input of shape 1×8×8 into 8×8×8 features, pools to 8×4×4, applies another convolution to obtain 16×4×4, and pools to 16×2×2. Flattening produces 64 values for a classifier with ten output scores. A batch of 64 images retains its outer batch axis throughout, ending in shape 64×10. These shapes expose what each convolution, pooling operation, and classification head does. They also provide a practical check for channel-order mistakes or an incorrectly chosen flattening dimension.

## Train on real handwriting and inspect the result

The program loads 1,797 handwritten digit images bundled with scikit-learn, corresponding to part of the UCI Optical Recognition of Handwritten Digits dataset. Fixed, class-stratified random splits allocate 1,077 images to training, 360 to validation, and 360 to testing. The experiment evaluates a random split of this image collection. A question about generalization to new writers calls for a writer-based split. Identifying the sampling unit gives an accuracy value a specific interpretation.

$$
p_k=\frac{e^{z_k}}{\sum_{j=1}^{C}e^{z_j}},\qquad L=-\log p_y
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/f1f09f167fed981a770e43fb.svg) | Unnormalized score for class k of one example, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/91b341df17f3af250f29c760.svg) | Class count, queried class index, and summation index; C=10 here. |
| ![Formula](https://ml-biomat.com/static/agent-math/40d617a7a3c0b027a60beb5b.svg) | Predicted probability of class k; probabilities sum to one. |
| ![Formula](https://ml-biomat.com/static/agent-math/1d9b846cface9f9348e4081a.svg) | Integer index of the true class; a separate local definition from the preceding output tensor. |
| ![Formula](https://ml-biomat.com/static/agent-math/d6d6d77928d04cf5f40c95e5.svg) | Single-example cross entropy, natural logarithm, and natural-exponential base; loss measured in nats. |

If all ten scores are zero, exponentials are all one, the true-class probability is 0.1, and loss is approximately 2.30259. Setting only the true score to ln9 gives probability 9/(9+9)=0.5 and loss approximately 0.69315. Raising its relative score reduces the loss. The library combines log and softmax stably, then averages example losses over a batch.

The network produces ten unnormalized scores. Classification cross entropy compares the score of the true class with those of the alternatives. PyTorch’s loss accepts these scores and integer labels directly and performs the combined calculation stably, so the training code does not apply an additional softmax first. Prediction can select the largest score; probability displays require normalization. Each image has one integer class label. Its 64 pixel positions are input measurements, not 64 separate classification targets.

### Complete Python: handwriting, feature maps, shifts, and transfer

Requires NumPy, Matplotlib, scikit-learn, and PyTorch. Run python main.py --output results --language en. Data are bundled with sklearn; no pretrained weight download is needed. The script trains two ten-class models plus source/target transfer models, producing four SVG figures, parameter files, summary.json, and traceable sample indices.

```
"""Small CNN, shift robustness, and transfer learning on public 8x8 digits."""
from pathlib import Path
import argparse,copy,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import torch
from torch import nn
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import sklearn

class TinyCNN(nn.Module):
    def __init__(self,classes=10):
        super().__init__();self.conv1=nn.Conv2d(1,8,3,padding=1);self.conv2=nn.Conv2d(8,16,3,padding=1)
        self.pool=nn.MaxPool2d(2);self.head=nn.Linear(16*2*2,classes)
    def features(self,x):return self.pool(torch.relu(self.conv2(self.pool(torch.relu(self.conv1(x))))))
    def forward(self,x):return self.head(self.features(x).flatten(1))

def shift(images,dy,dx):
    # Zero padding, never wrap pixels across the opposite image boundary.
    p=nn.functional.pad(images,(1,1,1,1));return p[:,:,1-dy:9-dy,1-dx:9-dx]

def train(model,tx,ty,vx,vy,epochs=50,augment=False,lr=.01):
    opt=torch.optim.Adam([p for p in model.parameters() if p.requires_grad],lr=lr)
    generator=torch.Generator().manual_seed(122);rng=np.random.default_rng(123)
    best=float('inf');saved=None;history=[];best_epoch=0
    for epoch in range(1,epochs+1):
        model.train()
        for ids in torch.randperm(len(tx),generator=generator).split(64):
            batch=tx[ids]
            if augment:
                dy,dx=rng.integers(-1,2,2);batch=shift(batch,int(dy),int(dx))
            opt.zero_grad(set_to_none=True);loss=nn.functional.cross_entropy(model(batch),ty[ids]);loss.backward();opt.step()
        model.eval()
        with torch.no_grad():
            logits=model(vx);vl=float(nn.functional.cross_entropy(logits,vy));accuracy=float((logits.argmax(1)==vy).float().mean())
            tl=float(nn.functional.cross_entropy(model(tx),ty))
        history.append([epoch,tl,vl,accuracy])
        if vl<best:best=vl;best_epoch=epoch;saved=copy.deepcopy(model.state_dict())
    model.load_state_dict(saved);model.eval();return np.array(history),best_epoch

def evaluate(model,x,y):
    with torch.no_grad():pred=model(x).argmax(1)
    return float((pred==y).float().mean()),pred.numpy()

def run(output,language):
    output.mkdir(parents=True,exist_ok=True);torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
    zh=language=='zh';tr=lambda z,e:z if zh else e
    plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none'})
    digits=load_digits();x=torch.tensor(digits.images[:,None]/16,dtype=torch.float32);y=torch.tensor(digits.target,dtype=torch.long)
    train_ids,held_ids=train_test_split(np.arange(len(y)),test_size=720,stratify=digits.target,random_state=120)
    val_ids,test_ids=train_test_split(held_ids,test_size=360,stratify=digits.target[held_ids],random_state=121)
    tx,ty=x[train_ids],y[train_ids];vx,vy=x[val_ids],y[val_ids];ex,ey=x[test_ids],y[test_ids]
    models={};histories={};metrics={}
    for name,augmentation in [('standard',False),('augmented',True)]:
        torch.manual_seed(124);model=TinyCNN();history,best=train(model,tx,ty,vx,vy,augment=augmentation)
        acc,pred=evaluate(model,ex,ey);shift_acc,_=evaluate(model,shift(ex,0,1),ey)
        models[name]=model;histories[name]=history;metrics[name]={'test_accuracy':acc,'shift_right_accuracy':shift_acc,'best_epoch':best}
        torch.save(model.state_dict(),output/f'{name}.pt')
    model=models['standard'];acc,pred=evaluate(model,ex,ey);cm=confusion_matrix(ey,pred,labels=range(10))
    errors=np.flatnonzero(pred!=ey.numpy());correct=np.flatnonzero(pred==ey.numpy())
    gallery=np.concatenate([errors[:10],correct[:max(0,20-len(errors[:10]))]])
    fig,axes=plt.subplots(4,5,figsize=(10,8),layout='constrained')
    for ax,ix in zip(axes.flat,gallery):
        ax.imshow(ex[ix,0],cmap='gray_r',vmin=0,vmax=1,interpolation='nearest')
        color='#A65327' if pred[ix]!=int(ey[ix]) else '#147566'
        ax.set_title(tr(f'真{int(ey[ix])} → 预测{pred[ix]}',f'True {int(ey[ix])} → predicted {pred[ix]}'),color=color,fontsize=10)
        ax.set_xticks([]);ax.set_yticks([])
        for sp in ax.spines.values():sp.set_visible(True);sp.set_edgecolor(color);sp.set_linewidth(1.5)
    fig.savefig(output/f'gallery-{language}.svg');plt.close(fig)
    fig=plt.figure(figsize=(12,7.8),layout='constrained');gs=fig.add_gridspec(2,2,width_ratios=[1.1,1])
    ax=fig.add_subplot(gs[:,0]);im=ax.imshow(cm,cmap='Blues')
    for r in range(10):
        for c in range(10):
            if cm[r,c]:ax.text(c,r,str(cm[r,c]),ha='center',va='center',color='white' if cm[r,c]>20 else '#17323c')
    ax.set(xticks=range(10),yticks=range(10),xlabel=tr('预测类别','Predicted class'),ylabel=tr('真实类别','True class'));fig.colorbar(im,ax=ax,shrink=.5,label=tr('样本数','Count'))
    ax=fig.add_subplot(gs[0,1])
    for name,color in [('standard','#0072B2'),('augmented','#D58500')]:ax.plot(histories[name][:,0],histories[name][:,2],color=color,label=tr('普通训练' if name=='standard' else '平移增强',name))
    ax.set(xlabel=tr('训练轮数','Epoch'),ylabel=tr('验证交叉熵','Validation cross entropy'));ax.legend()
    ax=fig.add_subplot(gs[1,1]);positions=np.arange(2)
    for offset,(name,color) in zip([-.18,.18],[('standard','#0072B2'),('augmented','#D58500')]):
        vals=[metrics[name]['test_accuracy'],metrics[name]['shift_right_accuracy']];ax.bar(positions+offset,vals,width=.34,color=color,label=tr('普通训练' if name=='standard' else '平移增强',name))
        for j,v in enumerate(vals):ax.text(j+offset,v+.015,f'{v:.1%}',ha='center',fontsize=9)
    ax.set(xticks=positions,xticklabels=[tr('原图','Original'),tr('右移1像素','Right shift: 1 pixel')],ylim=(0,1.12),ylabel=tr('测试准确率','Test accuracy'));ax.legend(loc='lower left')
    fig.savefig(output/f'results-{language}.svg');plt.close(fig)
    # One correctly classified digit 8; all maps from its actual trained forward pass.
    ix=int(next(i for i in correct if int(ey[i])==8));sample=ex[ix:ix+1]
    with torch.no_grad():kernels=model.conv1.weight[:,0].numpy();maps=torch.relu(model.conv1(sample))[0].numpy()
    fig=plt.figure(figsize=(13,4),layout='constrained');gs=fig.add_gridspec(2,9)
    ax=fig.add_subplot(gs[:,0]);ax.imshow(sample[0,0],cmap='gray_r',vmin=0,vmax=1);ax.set_title(tr('输入8','Input 8'));ax.axis('off')
    wmax=float(np.abs(kernels).max());amax=float(maps.max())
    top=[];bottom=[]
    for j in range(8):
        ax=fig.add_subplot(gs[0,j+1]);imw=ax.imshow(kernels[j],cmap='RdBu_r',vmin=-wmax,vmax=wmax,interpolation='nearest');ax.set_title(f'{j}');ax.axis('off');top.append(ax)
        ax=fig.add_subplot(gs[1,j+1]);ima=ax.imshow(maps[j],cmap='magma',vmin=0,vmax=amax,interpolation='nearest');ax.axis('off');bottom.append(ax)
    fig.colorbar(imw,ax=top,shrink=.6,label=tr('卷积核权重','Kernel weight'));fig.colorbar(ima,ax=bottom,shrink=.6,label=tr('ReLU响应','ReLU response'))
    fig.savefig(output/f'features-{language}.svg');plt.close(fig)
    # Transfer from digits 0--4 to different target classes 5--9.
    source_train=ty<5;source_val=vy<5;torch.manual_seed(125);source=TinyCNN(5)
    train(source,tx[source_train],ty[source_train],vx[source_val],vy[source_val],epochs=40)
    rng=np.random.default_rng(126);few=np.concatenate([rng.choice(np.flatnonzero(ty.numpy()==k),20,replace=False) for k in range(5,10)])
    target_val=vy>=5;target_test=ey>=5;transfer={}
    for setting in ['scratch','frozen','finetune']:
        torch.manual_seed(127);target=TinyCNN(5)
        if setting!='scratch':
            target.conv1.load_state_dict(source.conv1.state_dict());target.conv2.load_state_dict(source.conv2.state_dict())
        if setting=='frozen':
            for p in list(target.conv1.parameters())+list(target.conv2.parameters()):p.requires_grad=False
        h,best=train(target,tx[few],ty[few]-5,vx[target_val],vy[target_val]-5,epochs=60,lr=.005)
        score,_=evaluate(target,ex[target_test],ey[target_test]-5)
        transfer[setting]={'test_accuracy':score,'best_epoch':best,'trainable_parameters':sum(p.numel() for p in target.parameters() if p.requires_grad)}
        torch.save(target.state_dict(),output/f'transfer-{setting}.pt')
    fig,ax=plt.subplots(figsize=(8,4.6),layout='constrained');labels=tr(['从头训练','冻结卷积特征','全部微调'],['From scratch','Frozen features','Fine-tuned features'])
    scores=[v['test_accuracy'] for v in transfer.values()];ax.bar(range(3),scores,color=['#89939b','#0072B2','#D58500'],width=.6)
    for j,score in enumerate(scores):ax.text(j,score+.015,f'{score:.1%}',ha='center')
    ax.set(xticks=range(3),xticklabels=labels,ylim=(0,1.12),ylabel=tr('目标类别5–9测试准确率','Target-class 5–9 test accuracy'))
    fig.savefig(output/f'transfer-{language}.svg');plt.close(fig)
    # Exact checks: cross-correlation window and zero-residual identity on nonnegative data.
    edge=torch.tensor([[-1.,0,1],[-1,0,1],[-1,0,1]]).view(1,1,3,3)
    image=torch.zeros(1,1,7,7);image[:,:,:,3:]=1;edge_result=nn.functional.conv2d(image,edge)
    assert float(edge_result[0,0,2,1])==3
    residual=nn.Conv2d(8,8,3,padding=1);nn.init.zeros_(residual.weight);nn.init.zeros_(residual.bias)
    positive=torch.rand(2,8,4,4);identity_error=float((torch.relu(positive+residual(positive))-positive).abs().max().detach());assert identity_error==0
    summary={'dataset':'sklearn bundled UCI optical digits','total':len(y),'splits':{'train':len(tx),'validation':len(vx),'test':len(ex)},'models':metrics,'parameter_count':sum(p.numel() for p in model.parameters()),'test_error_count':len(errors),'feature_sample_dataset_index':int(test_ids[ix]),'transfer_source_train_n':int(source_train.sum()),'transfer_target_train_n':len(few),'transfer_target_test_n':int(target_test.sum()),'transfer':transfer,'edge_manual_value':float(edge_result[0,0,2,1]),'zero_residual_identity_error':identity_error,'torch_version':torch.__version__,'sklearn_version':sklearn.__version__}
    (output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    np.savez(output/'experiment.npz',train_ids=train_ids,validation_ids=val_ids,test_ids=test_ids,predictions=pred,confusion=cm,kernels=kernels,maps=maps,gallery_ids=test_ids[gallery],few_shot_train_ids=train_ids[few],**{f'history_{k}':v for k,v in histories.items()})
    print(json.dumps(summary,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path('results'));p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args();run(a.output,a.language)
```

![Left: standard-model confusion counts on 360 test images. Upper right: validation cross entropy for both training settings. Lower right: test accuracy on original and one-pixel-right-shifted images. Both runs share initial weights and select their own parameters by validation loss.](https://ml-biomat.com/static/tutorials/machine-learning/figures/f020532e9da29fb95841f49e.svg?v=f020532e9da2)

Figure 2Left: standard-model confusion counts on 360 test images. Upper right: validation cross entropy for both training settings. Lower right: test accuracy on original and one-pixel-right-shifted images. Both runs share initial weights and select their own parameters by validation loss.

Standard training uses Adam, learning rate 0.01, batches of 64, and 50 epochs, retaining parameters by validation cross entropy. The model has 1,898 parameters and correctly classifies 354 of the 360 test images, giving 98.33% accuracy. Confusion-matrix rows are true classes and columns are predicted classes. Diagonal entries count correct predictions; off-diagonal entries identify particular confusions. An overall score gives the amount of error, while the matrix reveals where that error occurs among the classes.

![Test-image contact sheet: all six misclassifications followed by fourteen correct examples. Titles give true and predicted classes, with one grayscale range. Image data: E. Alpaydin and C. Kaynak, UCI Optical Recognition of Handwritten Digits, CC BY 4.0, loaded through scikit-learn.](https://ml-biomat.com/static/tutorials/machine-learning/figures/37d3a100d01b5bdf365e6a20.svg?v=37d3a100d01b)

Figure 3Test-image contact sheet: all six misclassifications followed by fourteen correct examples. Titles give true and predicted classes, with one grayscale range. Image data: E. Alpaydin and C. Kaynak, UCI Optical Recognition of Handwritten Digits, CC BY 4.0, loaded through scikit-learn.

The contact sheet shows the six errors first, followed by fourteen correct predictions, with a common intensity range for every image. Borders and titles identify true and predicted classes. Inspect whether strokes are faint, loops are broken, or local shapes resemble another digit. The selection rule keeps errors visible while preserving correct examples for comparison. Similar grouping in a real application can reveal relationships between errors and exposure, cropping, background, or annotation conventions, providing specific hypotheses for a further experiment.

## What does a bright feature-map region mean?

Every trained first-layer kernel contains a particular set of weights. Displaying those weights alongside responses to the same image shows how one input becomes several different feature maps. We select a correctly classified “8.” All kernels share a color scale centered at zero, and all response maps share another range. Their brightness differences therefore retain comparable numerical meaning instead of independently stretching every panel to maximum contrast. Comparing the original image, signed weights, and rectified responses connects visible patterns to the actual forward computation.

![A correctly classified digit 8, original dataset index 1069, and its first-layer responses. Top: eight trained kernels with one symmetric color scale. Bottom: eight ReLU feature maps with one nonnegative scale. Input intensity is 0–1; channel indices are 0–7.](https://ml-biomat.com/static/tutorials/machine-learning/figures/57fd50618776890e652adec3.svg?v=57fd50618776)

Figure 4A correctly classified digit 8, original dataset index 1069, and its first-layer responses. Top: eight trained kernels with one symmetric color scale. Bottom: eight ReLU feature maps with one nonnegative scale. Input intensity is 0–1; channel indices are 0–7.

A bright region means that a channel produced a large value at that position. It describes a match under that local computation, while later layers still combine, threshold, and weight the responses. The image alone does not quantify that region’s contribution to the final class decision. Naming a channel a “circle detector” calls for additional experiments across inputs. A useful next step is to compare examples or intervene through masking and feature changes, then separately examine the activation response and the resulting prediction.

![Diverse optimized inputs associated with one network unit. These are optimization-generated images, not natural photographs or outputs of our digit CNN. Original figure: Chris Olah, Alexander Mordvintsev, Ludwig Schubert, Feature Visualization, Distill, 2017, CC BY 4.0, unchanged.](https://ml-biomat.com/static/tutorials/machine-learning/figures/6bfaf9eb5121d82f51f687e7.png?v=6bfaf9eb5121)

Figure 5Diverse optimized inputs associated with one network unit. These are optimization-generated images, not natural photographs or outputs of our digit CNN. Original figure: Chris Olah, Alexander Mordvintsev, Ludwig Schubert, Feature Visualization, Distill, 2017, CC BY 4.0, unchanged.

The 2017 Distill article *Feature Visualization* optimized input images to find visual patterns that activate selected network components. The reproduced figure uses a diversity objective to display several patterns associated with the same unit. These are optimized images, whereas our handwritten panels display responses to observed data. One view fixes an input and follows computation forward; the other fixes a network objective and adjusts the input. Together they help explain why one channel’s behavior need not correspond to a single canonical photograph.

## Move images, then transfer features

Shifting every test image one pixel to the right, padding the left with zeros and discarding pixels that leave the right boundary, lowers standard-model accuracy from 98.33% to 82.78%. One pixel is an eighth of the width of these small images, so the intervention is substantial. It changes both stroke locations and edge information. Inspecting the transformed images helps interpret the result. Shared convolutional kernels have not removed the complete network’s dependence on position, pooling, and cropping.

The second model randomly chooses horizontal and vertical displacements from −1, 0, and 1 for each training batch, using zero padding rather than wrapping pixels around the opposite edge. Validation and testing retain their fixed procedures. This model achieves 96.11% on original images and 97.22% on right-shifted images. The measured tradeoff is specific: augmentation improves adaptation to the covered positional changes while also changing original-image performance. Choose augmentation strength and comparison priorities according to the variations expected during use.

Transfer learning changes where the features start. Train a source model, then reuse its representation for a target task so the target data need not establish every feature from the beginning. Freezing features trains only a new classification head. Fine-tuning allows some or all feature layers to adapt further. Similarity of local structure, target sample count, and the layers that require adaptation all affect this choice. Preprocessing and channel meaning must also match: adapting an RGB-pretrained model to grayscale inputs, for example, requires an explicit channel-conversion procedure.

![Source task 0–4 uses 541 training images. Target task 5–9 uses 20 per class, 100 total, with 179 test images. Target runs share head initialization, learning rate, and 60-epoch budget. Frozen features train 325 parameters; the other settings train 1,573.](https://ml-biomat.com/static/tutorials/machine-learning/figures/0ffdc984769bd2da889dda10.svg?v=0ffdc984769b)

Figure 6Source task 0–4 uses 541 training images. Target task 5–9 uses 20 per class, 100 total, with 179 test images. Target runs share head initialization, learning rate, and 60-epoch budget. Frozen features train 325 parameters; the other settings train 1,573.

Our source model sees only the 541 training images labeled 0–4 and uses the corresponding validation images to select its parameters. The target task contains digits 5–9, with twenty training examples per class, one hundred in total, and 179 test images. The three target models receive identical initial classification-head parameters and sixty training epochs. Frozen features achieve 93.85%, while training from scratch and fine-tuning both achieve 98.32%. The frozen model trains 325 parameters; the other two train 1,573. This exposes a concrete difference between computational restriction and adaptation, making the usefulness of existing features a measurable question.

A frozen representation may already contain relevant strokes yet organize them imperfectly for the new categories. Updating only the head can recombine available features but cannot change how those features are measured. Fine-tuning permits that change, while using a source model as its starting point. Training from scratch has the same final architecture without that starting representation. Keeping target labels, splits, head initialization, and training budget explicit helps separate these alternatives. Repeating a comparison across target sample counts would show how the value of the starting representation changes with available evidence.

## From convolution windows to image tokens

A Vision Transformer organizes images differently. It divides an image into patches, flattens each patch, and maps it into a common feature dimension. These image tokens exchange information through attention. A 224×224 RGB image divided into 16×16 patches yields 14×14 = 196 patches, each initially containing 16×16×3 = 768 values. Positional information distinguishes their locations, while a classification head combines the processed representation. The original Vision Transformer work, released in 2020, demonstrated this patch-sequence approach at large pretraining scale.

Convolution specifies a shared local rule for reading a neighborhood. Attention uses content-dependent weights to connect tokens. Both rely on data and training rules to learn useful representations, and hybrid networks can combine them. Local assumptions, resolution, dataset size, and computation budget affect the practical comparison. Evaluate alternatives under a shared task and explicit training conditions. The chapter on [attention, Transformers, and state-space models](https://ml-biomat.com/tutorials/machine-learning/m32/en/) develops queries, keys, values, and computational cost; the essential bridge here is how an image becomes a sequence of processable tokens.

For a new vision problem, follow the same sequence of questions. Inspect what images and labels actually represent, then establish spatial scale, channels, and boundaries. Build a runnable baseline, examine its confusion matrix and error images, test changes relevant to the intended application, and compare transfer strategies. Save data splits, intensity ranges, transformation order, parameters, and class names so that a new image passes through the same procedure. An image serves as model input, evidence about errors, and a route to understanding the computation itself.

[Download complete code and data](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M12.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Optical Recognition of Handwritten Digits — UCI](https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits)

   Data definition, original collection, and license.

   Dataset CC BY 4.0; E. Alpaydin and C. Kaynak
2. [scikit-learn — load_digits](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_digits.html)

   The bundled 1,797-example data and array structure.

   scikit-learn BSD-3-Clause; dataset attribution separate
3. [PyTorch — Conv2d](https://docs.pytorch.org/docs/2.15/generated/torch.nn.Conv2d.html)

   Cross-correlation convention, weight shapes, and boundary parameters.
4. [Dive into Deep Learning — LeNet](https://d2l.ai/chapter_convolutional-neural-networks/lenet.html)

   Handwriting recognition and local shared computation.

   CC BY-SA 4.0; original explanatory prose here
5. [Deep Residual Learning for Image Recognition](https://arxiv.org/abs/1512.03385)

   Original residual-network research.

   Primary-paper link; no paper figure copied
6. [Feature Visualization](https://distill.pub/2017/feature-visualization/)

   Reproduced original figure and optimized-input interpretation.

   CC BY 4.0; Olah, Mordvintsev, Schubert
7. [An Image is Worth 16x16 Words](https://arxiv.org/abs/2010.11929)

   Image patches and Vision Transformers.

   Primary-paper link; no paper figure copied
