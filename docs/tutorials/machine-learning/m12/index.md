# 让图像成为可计算的结构：卷积、残差与迁移

Source: https://ml-biomat.com/tutorials/machine-learning/m12/
Language: zh-CN

从九个乘积读懂一个像素响应，再用真实手写图像观察网络怎样识别、犯错和适应变化。

## 同一个数字，换个位置还能认出来吗

在纸上写一个“8”，再把纸向右挪一点，我们通常仍能认出它。对计算机来说，移动却改变了许多像素的位置。如果直接把整幅图展开成长向量，再交给全连接网络，每个位置都会连接一组独立权重；同一种短横线出现在左上角与右下角时，模型可能需要分别学习它们。卷积网络从图像的空间结构出发，把“局部图案可能在不同位置重复出现”这个认识写进模型。

本章用真实的手写数字图像回答三个相连的问题：卷积核怎样把像素变成局部特征，局部特征怎样组成整幅图的分类结果，已经学到的特征怎样迁移到新的类别。除了训练一个小型CNN，我们还会把测试图像右移一个像素，检查准确率怎样变化；再让模型先学习数字0到4，随后用少量数字5到9的样本比较冻结特征、继续微调和从头训练。图像处理、分类评价与迁移由同一套可运行实验串起来。

一幅灰度图可以看成二维数表，每个数描述一个位置的亮度或强度。彩色RGB图在每个位置有红、绿、蓝三个通道，因此通常需要三个这样的数表。通道不是三张互不相关的照片，而是同一空间位置的不同测量。相机图像还涉及曝光、编码与颜色空间；本章的数据更简单：每张图有8×8个整数，取值0到16，来自原始手写图像局部块内的像素计数。代码将它们除以16，得到零到一之间的无量纲输入。

## 一张小模板怎样读完整幅图

设想拿一张带有九个权重的3×3模板，覆盖图像的一小块。把对应位置的像素与权重相乘，再把九个乘积相加，就得到这一个位置的响应。模板向右移动，再计算一次，逐行扫过图像后便得到一幅新的数表，称为特征图。同一组九个权重在所有位置反复使用，这就是参数共享。训练时，梯度会把各位置对同一权重的贡献累加起来，使这个模板逐渐适应任务。

$$
Y_{o,r,s}=b_o+\sum_{c=1}^{C_{\mathrm{in}}}\sum_{u=0}^{k_h-1}\sum_{v=0}^{k_w-1}K_{o,c,u,v}\,X_{c,r+u,s+v}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/871a117fa007ef6935e35aae.svg) | 输入张量：通道数×高度×宽度；本章强度除以16后无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/14682edf48bc589a68dff1f5.svg) | 学习得到的核权重，含输出通道、输入通道与两个空间维度。 |
| ![Formula](https://ml-biomat.com/static/agent-math/4def0809683bf7be8e0840a2.svg) | 输出通道o在行r列s的响应，以及该通道的偏置，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/3ec52b56ebfaa3600a766fc6.svg) | 输入通道索引、核内行索引、核内列索引。 |
| ![Formula](https://ml-biomat.com/static/agent-math/39dd0476c806711eec2d3db1.svg) | 输入/输出通道数、核的高宽、输入高宽，均为计数。 |

此式对应步幅1、无填充且不翻转核的互相关。单通道3×3小块每行(0,0,1)，核每行(−1,0,1)，偏置0时，三个行和均为1，总响应3。多输入通道时，把各通道同样算出的响应继续相加；同一组核权重在不同r、s处共享。

例如模板的每一行都是(−1,0,1)，覆盖的图像小块每一行都是(0,0,1)。每行计算为−1×0＋0×0＋1×1＝1，三行相加为3。这个模板对从暗到亮的竖直边界产生正响应；把亮暗方向反过来，响应会变成负值；覆盖均匀区域时，正负权重相互抵消，结果为零。它像一个测量局部变化的小仪器，运算含义可以逐格检查。

深度学习库通常把不翻转模板的互相关运算也称为卷积，本章的公式与PyTorch采用这个约定。学习得到的模板没有必须朝某个方向的先验标签，因此这项命名约定不妨碍训练，但手算时需要和库保持一致。对于多通道输入，一个输出通道会同时读取所有输入通道，把每个通道的局部乘积求和，再加一个偏置。多个输出通道拥有不同的权重，因而能对不同局部模式作出响应。

$$
P=C_{\mathrm{out}}\bigl(C_{\mathrm{in}}k_hk_w+1\bigr)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/1aaddf0d4be4d873ff6c0600.svg) | 带偏置普通卷积层的参数总数，整数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/6e8ea1ef1c2843b67d533a09.svg) | 输入与输出通道数；本式不使用分组卷积。 |
| ![Formula](https://ml-biomat.com/static/agent-math/b75fe22b20830182aee39fbd.svg) | 卷积核的高和宽，以像素位置数计。 |
| ![Formula](https://ml-biomat.com/static/agent-math/95836ae470c61ab15bfb67d6.svg) | 每个输出通道额外的一个偏置参数。 |

每个输出通道需要C_in组空间核，以及一个偏置。第一层1→8通道、3×3核共有80参数；第二层8→16通道共有1168参数；64→10分类头有650参数，总计1898。图像高宽影响计算位置数，但不直接进入这项共享参数计数。

若输入只有一个通道，使用八个3×3卷积核并带偏置，需要8×(1×3×3＋1)＝80个参数。输入图像从8×8扩大到80×80时，这一层的参数数目仍然是80，只是需要在更多位置执行运算。这种结构把“相同局部规则可在不同位置使用”的假设转化为计算上的共享，也解释了卷积为何特别适合具有网格邻近关系的图像、时频图和规则采样场。

## 边界、步幅与逐渐扩大的视野

模板滑到边缘时，有一部分会落到原图之外。有效卷积只保留模板完全落在图内的位置，因此输出会缩小；填充则在边缘添加额外数值，让模板也能围绕原来的边界位置计算。零填充把图外值设为零，反射填充则把边缘附近的值镜像延伸。两者包含不同的边界假设，在数字识别中可以作为模型设置，在测量图像或物理场中则要与实际边界含义对应。

$$
n_{\mathrm{out}}=\left\lfloor\frac{n+2p-k}{S}\right\rfloor+1,\qquad r_\ell=r_{\ell-1}+(k_\ell-1)j_{\ell-1},\quad j_\ell=S_\ell j_{\ell-1}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/081412c66cbf83929b8e1b9c.svg) | 沿一个空间方向的输入长度、输出长度，以网格点计。 |
| ![Formula](https://ml-biomat.com/static/agent-math/4ae3f422930e98f3a99ecff2.svg) | 每侧填充数、核宽度、正整数步幅；此式膨胀率为1。 |
| ![Formula](https://ml-biomat.com/static/agent-math/e324cf06f94b000228b474a7.svg) | 向下取整，保留能够完整计算的位置数。 |
| ![Formula](https://ml-biomat.com/static/agent-math/09151dc95553bb8667adfd37.svg) | 当前层编号及其核宽与步幅。 |
| ![Formula](https://ml-biomat.com/static/agent-math/9c233bd6c4b9d9308fa08b8a.svg) | 感受野宽度、相邻特征位置在原图上的间隔，均以原图像素计。 |
| ![Formula](https://ml-biomat.com/static/agent-math/ebb617a8dcc5fd9713b9310d.svg) | 输入层的初始范围和间隔；填充部分计入名义感受野。 |

沿高、宽方向分别应用长度式。n=8、p=1、k=3、S=2得到floor(7/2)+1=4。感受野每层增加(k−1)个上层位置间隔：3×3卷积后r=3、j=1；2×2步幅2池化后r=4、j=2；再卷积后r=8；再池化后r=10、j=4。

步幅决定模板每次移动几个像素。8×8输入使用3×3核、步幅1、四周各补1个像素，输出仍为8×8；步幅改为2，则输出为4×4。最大池化又是另一种局部操作：取窗口中的最大值，突出窗口里较强的响应；平均池化则取平均。对数值为1、3、2、4的2×2小块，最大池化输出4，平均池化输出2.5。池化没有学习权重，但会改变空间分辨率及后续能保留的细节。

一个深层特征位置依赖原图多大范围，称为它的感受野。第一层3×3卷积看到3×3范围，再接一个步幅1的3×3卷积，会把范围扩大到5×5。若中间经过降采样，后续每个位置对应原图上更大的间隔，感受野扩大得更快。本章网络经过卷积、池化、卷积、池化，名义感受野依次为3、4、8、10个像素；最后的10包含填充区域，而原始图像只有8个像素宽。这说明结构上的覆盖范围与真正观测到的图像内容需要分开理解。

共享模板使特征图在理想条件下能够跟随输入一起移动，这叫平移等变；整幅图的分类答案在移动后保持相同，则是平移不变。边界、池化和步幅都会影响这种关系。卷积提供了有用的结构基础，却不会自动让整个分类器对任意移动完全不敏感。后面的实际平移实验将把这个区别变成可测量的准确率变化。

## 逐格算一幅特征图

左侧7×7图像中，右半部分为1，左半部分为0。点击像素可改变输入；选择核、步幅与填充，右侧立刻重新计算。橙框标出当前输出所读的输入范围，中间九个乘积逐项相加。像素格和输出格均可用键盘选择，回车或空格执行。

[Figure: 可编辑输入、卷积核与输出](https://ml-biomat.com/tutorials/machine-learning/m12/#M12-plot)

行列索引从0开始；橙框外的图外位置按零计算。输出颜色表示响应符号和大小，精确值直接写在格内；局部平均核的每个权重为1/9。

## 从局部笔画走向深层网络

卷积之后接非线性激活，再逐步组合局部响应，便形成CNN。较浅层接触小范围像素，较深层组合更广范围的信息；这种逐层处理使网络能够用有限参数表达复杂的图像关系。早期的LeNet把局部连接、共享权重和降采样用于手写识别，将这些设计组织成端到端训练的系统。今天读取支票、识别文档或分析显微图像的任务虽然规模不同，仍然能从这套局部到整体的计算思路出发理解。

网络加深后，优化也变得困难。He等人在2015年公开的残差网络工作，把一个模块的目标改写为学习输入的修正量，再将修正量与原输入相加。如果模块暂时不需要改变输入，残差分支接近零就能保留原表示。直接路径同时给信息和梯度提供了另一条通路，使深层网络的构建更容易。这个想法后来也出现在Transformer和图神经网络中，因为它处理的是多层变换中的信息传递问题。

$$
z=x+F(x;\theta),\qquad y=\operatorname{ReLU}(z)
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/d52903f55ffbb1e8eaaa0191.svg) | 输入、相加后的张量、激活后的输出，形状相同；本例无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/2e7656feccc67098b1dc854a.svg) | 参数θ控制的残差分支，输出为需要加到输入上的修正量。 |
| ![Formula](https://ml-biomat.com/static/agent-math/f1869de26e07bd8042e214a7.svg) | 逐元素保留正值、将负值置零的激活。 |

若x=(0.8,0.4)、残差为(−0.2,0.1)，相加后为(0.6,0.5)，ReLU保持这些正值。残差为零且输入非负时，输出等于输入；负输入经过最后的ReLU会改变。若分支形状不同，先用投影把捷径变为匹配形状，再做逐元素加法。

![残差模块的计算分路：上方学习修正量，下方直接传递输入，在相加处合并并经过ReLU。数值例采用非负输入；蓝色直接路径和橙色修正路径共同组成输出。此图按计算定义原创绘制。](https://ml-biomat.com/static/tutorials/machine-learning/figures/322bb543e033f7d83192e531.svg?v=322bb543e033)

图 1残差模块的计算分路：上方学习修正量，下方直接传递输入，在相加处合并并经过ReLU。数值例采用非负输入；蓝色直接路径和橙色修正路径共同组成输出。此图按计算定义原创绘制。

相加要求两条分支具有相同形状。如果空间尺寸或通道数改变，捷径分支可以通过1×1卷积及合适步幅匹配形状；这种投影有自己的参数。相加之后是否再使用ReLU，也会影响恒等关系的精确条件。本章代码在非负输入上把残差卷积权重与偏置设为零，计算相加后的ReLU，验证输出与输入的最大差为零。这是一个可以单独检查的结构算例，完整训练部分则使用两层卷积的小网络。

这套小网络先把1×8×8图像变成8×8×8特征，再池化成8×4×4；第二次卷积得到16×4×4，再池化成16×2×2。最后展平成64个数，送入输出十个分数的分类层。若一次输入64张图，最外面的批维始终保留，最终输出形状为64×10。卷积层、池化层和分类头各自的作用由这些形状直接呈现，检查它们也能及时发现通道顺序或展平维度错误。

## 用真实手写图像训练并核对结果

程序读取scikit-learn随库提供的1797张手写数字图像，它们对应UCI Optical Recognition of Handwritten Digits数据的一部分。我们按类别分层随机划出1077张训练图、360张验证图和360张测试图，固定划分种子。这里研究的是这批图像上的随机划分任务；若研究新书写者的泛化，需要进一步按书写者身份组织划分。明确样本单位之后，准确率才对应一个清楚的问题。

$$
p_k=\frac{e^{z_k}}{\sum_{j=1}^{C}e^{z_j}},\qquad L=-\log p_y
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/f1f09f167fed981a770e43fb.svg) | 一个样本在类别k上的未归一化分数，无量纲。 |
| ![Formula](https://ml-biomat.com/static/agent-math/91b341df17f3af250f29c760.svg) | 类别数、待查看类别索引、求和索引；本章C=10。 |
| ![Formula](https://ml-biomat.com/static/agent-math/40d617a7a3c0b027a60beb5b.svg) | 类别k的预测概率，各类别相加为1。 |
| ![Formula](https://ml-biomat.com/static/agent-math/1d9b846cface9f9348e4081a.svg) | 该样本真实类别的整数索引，与前式输出张量符号属于不同局部定义。 |
| ![Formula](https://ml-biomat.com/static/agent-math/d6d6d77928d04cf5f40c95e5.svg) | 单样本交叉熵、自然对数、自然指数底；损失单位为nats。 |

若十个分数全为0，各指数都为1，正确类概率为0.1，损失约2.30259。若正确类分数为ln9，其余仍为0，概率为9/(9+9)=0.5，损失约0.69315。提高正确类相对分数会减少损失。库把log与softmax合并计算以提高数值稳定性，批损失再对样本取平均。

网络输出十个未经归一化的分数，交叉熵损失将正确类别的分数与其他类别比较。PyTorch的分类交叉熵直接接收这些分数和整数类别标签，内部完成稳定的计算，因此代码在训练前不再额外调用softmax。预测时取最大分数对应的类别即可；若要展示类别概率，再进行归一化。每张图的标签是一个整数，不能把64个像素误当成64个监督目标。

### 完整Python：手写识别、特征响应、平移与迁移

依赖NumPy、Matplotlib、scikit-learn、PyTorch；运行python main.py --output results --language zh。数据由sklearn随库提供，无需额外下载权重。程序实际训练两个十分类模型及源/目标迁移模型，产生四组SVG、参数文件、summary.json和可追溯样本索引。

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

![左：普通模型在360张测试图上的混淆计数。右上：两种训练方式的验证交叉熵；右下：原图与右移1像素图的测试准确率。普通/增强训练均从相同初始参数开始，各按验证误差选择参数。](https://ml-biomat.com/static/tutorials/machine-learning/figures/9fea534e20151cf751b4ead5.svg?v=9fea534e2015)

图 2左：普通模型在360张测试图上的混淆计数。右上：两种训练方式的验证交叉熵；右下：原图与右移1像素图的测试准确率。普通/增强训练均从相同初始参数开始，各按验证误差选择参数。

普通训练使用Adam、学习率0.01、批大小64，运行50轮并按验证交叉熵保存参数。模型共有1898个参数，在360张测试图中正确识别354张，准确率98.33%。混淆矩阵按真实类别排列行、预测类别排列列，主对角线表示正确结果，离开主对角线的数值指出具体混淆。总体分数告诉我们错误有多少，矩阵则告诉我们哪些类别之间更容易发生错误。

![测试图像接触表：先列出全部六张误分类图，再列出十四张正确图。标题给出真实类别与预测类别，统一灰度范围。图像数据：E. Alpaydin、C. Kaynak，UCI Optical Recognition of Handwritten Digits，CC BY 4.0；由scikit-learn载入。](https://ml-biomat.com/static/tutorials/machine-learning/figures/6ca529bf85b397ae30e77d3e.svg?v=6ca529bf85b3)

图 3测试图像接触表：先列出全部六张误分类图，再列出十四张正确图。标题给出真实类别与预测类别，统一灰度范围。图像数据：E. Alpaydin、C. Kaynak，UCI Optical Recognition of Handwritten Digits，CC BY 4.0；由scikit-learn载入。

图像接触表先显示这次测试的六张错误图，再补入十四张正确图，所有像素都按相同范围显示。边框和标题给出真实类别与预测类别，便于检查某些笔画是否模糊、闭环是否断开、局部形状是否接近另一个数字。这个选择规则使错误可见，也让我们保留正确样本作为参照。对实际数据，类似的分组检查还能揭示曝光、裁剪、背景或标注方式与错误之间的联系。

## 特征图亮起来，究竟说明什么

在训练后的第一层中，每个卷积核都有一组具体权重。把这些权重画出来，再把同一张数字图经过各卷积核和ReLU后的响应并排展示，就能看到模型怎样把同一输入转成不同数表。本章选取一张正确识别的“8”，所有核使用同一个以零为中心的色标，所有响应图也共用一个范围。这样亮暗差异保留了可比较的数值含义，而不只是把每幅图各自拉满对比度。

![一张正确识别的数字8及其第一层响应，原数据索引1069。上排为八个实际训练核，统一对称色标；下排为ReLU后的八张特征图，统一非负色标。输入按0–1显示；通道编号0–7。](https://ml-biomat.com/static/tutorials/machine-learning/figures/b9f0a182fef413d64411987d.svg?v=b9f0a182fef4)

图 4一张正确识别的数字8及其第一层响应，原数据索引1069。上排为八个实际训练核，统一对称色标；下排为ReLU后的八张特征图，统一非负色标。输入按0–1显示；通道编号0–7。

响应图中的亮区表示这个通道在相应位置输出较大数值。它告诉我们输入与该局部计算的匹配情况，但还没有回答“这个位置对最终分类贡献多少”。后续层会继续组合、截断和加权这些响应。把某张响应图直接命名为“识别圆圈的神经元”，需要额外实验支持；更有效的起点是比较不同输入、遮挡区域或特征干预之后，响应与最终预测分别怎样改变。

![同一网络单元对应的多种优化输入图像，展示增加多样性目标后的视觉模式；这些不是自然照片，也不是本章数字CNN生成的样本。原图：Chris Olah、Alexander Mordvintsev、Ludwig Schubert，Feature Visualization，Distill，2017，CC BY 4.0，未改动。](https://ml-biomat.com/static/tutorials/machine-learning/figures/6bfaf9eb5121d82f51f687e7.png?v=6bfaf9eb5121)

图 5同一网络单元对应的多种优化输入图像，展示增加多样性目标后的视觉模式；这些不是自然照片，也不是本章数字CNN生成的样本。原图：Chris Olah、Alexander Mordvintsev、Ludwig Schubert，Feature Visualization，Distill，2017，CC BY 4.0，未改动。

2017年的Distill文章《Feature Visualization》用优化输入图像的方法，寻找能激活指定网络单元的视觉模式。这里保留的原图通过多样性目标展示同一个单元对应的多种图案。它们是由优化过程得到的图像，与前面真实手写样本的特征响应属于不同证据：一个从固定输入向前观察，另一个固定网络目标、反过来调整输入。两种视角放在一起，能帮助我们避免把一个通道的作用理解成一张唯一的“标准照片”。

## 移动图像与迁移特征

将全部测试图向右移动一个像素，用零填补左侧、移出右边界的像素直接舍弃，普通模型的准确率从98.33%降到82.78%。在8×8图像上，一个像素已经占宽度的八分之一，这是一项明确而较强的变化。它同时改变笔画位置和边缘信息，所以应通过实际变换后的图像理解结果。卷积核共享，并没有消除整个网络对位置、池化与裁剪的依赖。

第二个模型在每个训练批次随机选择横向、纵向各−1、0或1像素的移动，使用零填充而非首尾循环。验证与测试流程保持固定。它在原图上的准确率为96.11%，在右移图上为97.22%。这组结果呈现了一个具体的训练取舍：在本次配置中，增强提高了对所覆盖位置变化的适应，同时改变了原图表现。选择增强强度时，应根据实际使用中会遇到的图像变化来决定比较重点。

迁移学习则改变特征的起点。先在源任务上训练网络，再把其中的表示用于目标任务，可以减少目标数据需要从零学起的内容。冻结特征时，只训练新的分类头，原卷积层不更新；微调则允许部分或全部特征继续适应新任务。源图像与目标图像的局部结构是否相似、目标样本有多少、哪些层需要改变，会共同影响选择。预处理和通道含义也要匹配，例如RGB预训练网络接收灰度图时需要明确通道转换方案。

![源任务0–4使用541张训练图；目标任务5–9每类20张，共100张，测试179张。三种目标方式使用相同分类头初始化、学习率与60轮预算。冻结方式训练325个参数，另两种训练1573个。](https://ml-biomat.com/static/tutorials/machine-learning/figures/5e87742ce57461b572e73797.svg?v=5e87742ce574)

图 6源任务0–4使用541张训练图；目标任务5–9每类20张，共100张，测试179张。三种目标方式使用相同分类头初始化、学习率与60轮预算。冻结方式训练325个参数，另两种训练1573个。

本章的源模型只使用训练划分中数字0到4的541张图，并用相应验证图选择参数。目标任务为数字5到9，每类从训练划分抽20张，共100张；测试包含179张目标图。三种目标模型的新分类头采用相同初始参数，统一训练60轮。冻结特征的准确率为93.85%，从头训练与全部微调均为98.32%；冻结模型只训练325个参数，另两者训练1573个。这个例子显示了计算与适应能力的差别，也使“已有特征是否帮到当前任务”成为可以实际比较的问题。

冻结表示中可能已经包含有用笔画，却未必按目标类别最合适的方式组织。只更新分类头能够重新组合已有特征，但无法改变这些特征怎样从像素中提取；微调允许继续改变提取规则，同时保留源任务提供的起点；从头训练则使用相同最终结构，从随机参数开始。保持目标标签、划分、分类头初始化与训练预算明确，才能分清这些选择。进一步改变目标样本数量，可以研究已有表示的价值怎样随可用数据增加而变化。

## 从卷积窗口走向图像词元

视觉Transformer采用另一种组织图像的方式：把图像分成小块，将每块像素展平成向量并映射到统一特征维度，得到图像词元，再通过注意力让不同位置交换信息。例如224×224的RGB图按16×16分块，会得到14×14＝196个块；每块原始向量含16×16×3＝768个数。位置编码帮助模型区分这些块在图像中的位置，分类头则汇总处理后的表示。2020年公开的Vision Transformer工作在大规模预训练条件下展示了这条分块序列路线。

卷积用共享的局部核规定一次运算如何读取邻域，注意力根据内容计算不同词元之间的联系。两种结构都需要数据与训练规则来学习有效表示，也可以组成混合网络。局部先验、输入分辨率、数据量和计算预算会影响实际表现；比较时应使用相同任务与清楚的训练条件。[注意力、Transformer与状态空间模型](https://ml-biomat.com/tutorials/machine-learning/m32/)一章会继续拆解查询、键、值及计算代价，本章先把图像怎样成为一组可处理的词元说清楚。

开始一个新的视觉任务时，可以沿本章的顺序工作：先看图像与标签实际描述什么，再确定空间尺度、通道和边界处理；用小网络建立可运行基线，检查混淆与错误图；随后用与应用相关的变换评价稳定性，并比较迁移方式。保存数据划分、强度范围、变换顺序、模型参数和类别表，让输入一张新图时能够重现同一处理过程。图像不是一张只用于展示的插图，它同时是模型输入、误差证据和理解计算机制的入口。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M12.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [Optical Recognition of Handwritten Digits — UCI](https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits)

   数据定义、原始采集与许可。

   Dataset CC BY 4.0; E. Alpaydin and C. Kaynak
2. [scikit-learn — load_digits](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_digits.html)

   本例随库数据的1797样本及数组结构。

   scikit-learn BSD-3-Clause; dataset attribution separate
3. [PyTorch — Conv2d](https://docs.pytorch.org/docs/2.15/generated/torch.nn.Conv2d.html)

   互相关约定、权重形状与边界参数。
4. [Dive into Deep Learning — LeNet](https://d2l.ai/chapter_convolutional-neural-networks/lenet.html)

   手写识别与局部共享计算的历史。

   CC BY-SA 4.0; original explanatory prose here
5. [Deep Residual Learning for Image Recognition](https://arxiv.org/abs/1512.03385)

   残差网络原始研究。

   Primary-paper link; no paper figure copied
6. [Feature Visualization](https://distill.pub/2017/feature-visualization/)

   原图与优化输入的解释。

   CC BY 4.0; Olah, Mordvintsev, Schubert
7. [An Image is Worth 16x16 Words](https://arxiv.org/abs/2010.11929)

   图像分块与视觉Transformer。

   Primary-paper link; no paper figure copied
