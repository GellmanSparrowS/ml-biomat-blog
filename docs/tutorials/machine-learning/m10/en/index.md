# Make training work: optimizers, scale, and generalization

Source: https://ml-biomat.com/tutorials/machine-learning/m10/en/
Language: en

From a hand-calculated update to measured network losses, gradients, and learning rates.

## The model is built. Why is learning still difficult?

Learning to ride a bicycle requires more than choosing the right direction. Turning too sharply creates a wobble; correcting too little lets the bicycle drift away. Training a neural network presents a related problem. A loss measures disagreement between predictions and targets, a gradient describes a local direction of change, and an optimizer converts that information into parameter updates. Even with the same network and data, update size, use of gradient history, and initial parameter scale can produce very different training curves.

Our running question is concrete: how can a network learn a curved relationship from noisy observations, train steadily, and retain predictive ability on new observations? We first examine SGD, momentum, and Adam on a two-dimensional landscape whose geometry is fully visible. We then train an actual multilayer network and record prediction error, gradient norms, and learning rates. The small landscape explains an update rule; the network’s measured training curves explain what happened in that experiment. Keeping these roles separate makes both kinds of evidence easier to read.

Training settings form a connected system. Initialization affects how signals enter deeper layers, normalization changes the scale of intermediate representations, regularization changes which details the network can rely on, and hyperparameter search determines how those choices are compared. A useful diagnostic process asks what changed, why it changed, and which observation would reveal its effect. By the end, you should be able to connect a training curve to its computation, design a small controlled comparison, and save the state required to resume or reproduce training.

## Turn a slope into one update

Imagine that the loss is a landscape and the parameters are coordinates on its map. The gradient points in the direction of greatest local increase, so its negative gives a local descent direction. The learning rate determines how far to move. Local information describes the neighborhood of the present point. A large step can cross a valley and land higher on its opposite side. Whether the loss falls is established by evaluating the updated parameters; choosing the negative gradient alone does not make every possible step size suitable.

$$
\theta_{t+1}=\theta_t-\eta g_t,\quad g_t=\frac1B\sum_{j\in\mathcal B_t}\nabla_\theta\ell_j(\theta_t);\qquad F(x,y)=\tfrac12(x^2+25y^2)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/579b56236a900400be4c8491.svg) | P model parameters before update t, dimensionless here. |
| ![Formula](https://ml-biomat.com/static/agent-math/34fcec286fec0105f96419d9.svg) | Positive learning rate controlling update size. |
| ![Formula](https://ml-biomat.com/static/agent-math/a8bc9a9919727860a99c5f29.svg) | Batch-mean gradient; ∇ collects partial derivatives with respect to parameters. |
| ![Formula](https://ml-biomat.com/static/agent-math/f55e53533c50f03e00925fd7.svg) | Batch size, set of current batch indices, and one sample index. |
| ![Formula](https://ml-biomat.com/static/agent-math/b3f25829030c7309d95691ef.svg) | Loss for sample j; squared error of a dimensionless target in our regression. |
| ![Formula](https://ml-biomat.com/static/agent-math/543e180ef21c4f915f1da00f.svg) | Separate two-dimensional teaching objective and its scalar coordinates, distinct from network parameters. |

Average gradients over the batch, then subtract the scaled result. The separate quadratic has gradient (x,25y). From (3,1), rate 0.07 gives (2.79,−0.75), reducing its objective from 17 to 10.9233 while crossing the valley in the steeper coordinate.

A full-data loss may average over millions of examples. Traversing all of them before every update can be expensive. Minibatch SGD uses the average gradient of a sampled group as an estimate of the full gradient, trading computational cost against sampling variation. A batch containing unusually difficult observations can temporarily increase the recorded loss. Shuffling avoids seeing examples in the same order each time, while sampling noise remains. When comparing curves, specify whether a point represents one minibatch or an evaluation over the same complete training or validation set.

Early work on stochastic approximation developed the broader idea of improving parameters using noisy local observations. For modern minibatch learning, the practical consequence is that update directions naturally fluctuate. Batch size, learning rate, and training duration should therefore be considered together. Smaller batches produce more parameter updates in one epoch. Conversely, the same number of updates can expose models to different numbers of examples. Recording epochs, batch size, and sample count makes the computational budget of a comparison much clearer.

![Sixty updates on F=(x²+25y²)/2, starting at (3,1). SGD and momentum use rate 0.07, momentum coefficient 0.6; Adam uses 0.15. Stars mark the minimizer and gray contours share levels. These are controlled update-rule experiments on an analytic objective.](https://ml-biomat.com/static/tutorials/machine-learning/figures/074c92d59a347a0f24001543.svg?v=074c92d59a34)

Figure 1Sixty updates on F=(x²+25y²)/2, starting at (3,1). SGD and momentum use rate 0.07, momentum coefficient 0.6; Adam uses 0.15. Stars mark the minimizer and gray contours share levels. These are controlled update-rule experiments on an analytic objective.

The illustrated valley is much steeper vertically than horizontally. Ordinary SGD can repeatedly cross the steep direction while advancing more slowly along the shallow one. The first update is easy to calculate: at coordinates (3, 1), the gradient is (3, 25), so a learning rate of 0.07 gives (2.79, −0.75). The vertical coordinate changes sign, showing that the step crosses the valley floor. The next vertical gradient changes sign too. Contours and trajectories together reveal where the repeated sideways motion comes from.

## Remember recent directions and adapt coordinate scales

Momentum adds a gradually forgetting accumulation of earlier gradients. If a component repeatedly points in the same direction, its contributions reinforce one another. If it alternates in sign, contributions partly cancel. A cart with inertia provides an intuitive analogy, although the optimizer’s “velocity” is an algorithmic variable rather than a physical speed. Because this variable stores update history, resuming a run requires the optimizer state as well as the model’s weights. Loading weights alone starts a different continuation of the learning process.

$$
v_t=\mu v_{t-1}+g_t,\qquad\theta_{t+1}=\theta_t-\eta v_t
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/c584295e8446c89497dad165.svg) | Current and preceding gradient accumulators, initialized to zero and matching parameter shape. |
| ![Formula](https://ml-biomat.com/static/agent-math/dab423e802bb7a0f16e23576.svg) | Dimensionless history-retention coefficient. |
| ![Formula](https://ml-biomat.com/static/agent-math/73bc71e9a241c8ca2cbf3b44.svg) | Current batch gradient, parameters, and positive learning rate; t indexes updates. |

Historical contributions receive another factor μ at each step. Two scalar gradients of 2 with μ=0.9 and zero initial accumulator give v=2 then 3.8, hence update magnitudes 0.2 and 0.38 at rate 0.1. If the second gradient is −2, the accumulator becomes −0.2 through partial cancellation. This convention does not multiply incoming gradients by (1−μ).

Adam also keeps separate estimates of the first and second moments of gradients. The first tracks recent direction; the second tracks recent squared magnitude for each parameter coordinate. Dividing by the square root of the latter adjusts updates to differences in coordinate scale. Kingma and Ba released their paper in late 2014 and presented it at ICLR in 2015. Its setting involved noisy, high-dimensional optimization with coordinates behaving at different scales. That motivation makes the familiar decay parameters easier to understand as parts of a mechanism.

$$
\begin{aligned}m_t&=\beta_1m_{t-1}+(1-\beta_1)g_t\\v_t&=\beta_2v_{t-1}+(1-\beta_2)g_t^{\odot2}\\\widehat m_t&=m_t/(1-\beta_1^t),\quad\widehat v_t=v_t/(1-\beta_2^t)\\\theta_{t+1}&=\theta_t-\eta\frac{\widehat m_t}{\sqrt{\widehat v_t}+\epsilon}\end{aligned}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/6547e8510550e1844593df44.svg) | Exponential accumulators of first and second raw gradient moments; v here accumulates squared gradients, unlike the preceding momentum notation. |
| ![Formula](https://ml-biomat.com/static/agent-math/d5c57a727bc90b1421a0594a.svg) | Two dimensionless history-retention coefficients. |
| ![Formula](https://ml-biomat.com/static/agent-math/3a6cadede5ab9cb27f1e8004.svg) | Coordinatewise squared gradient, not a vector inner product. |
| ![Formula](https://ml-biomat.com/static/agent-math/784f6a437e83ae47a34d6590.svg) | Moment estimates corrected for zero initialization. |
| ![Formula](https://ml-biomat.com/static/agent-math/3ec959b931716b50d217ab86.svg) | Parameter vector, learning rate, and update index starting at 1; exponent t denotes a power. |
| ![Formula](https://ml-biomat.com/static/agent-math/f24aa8f3e071190248b55b03.svg) | Positive stabilizer preventing division by zero; square root and division are coordinatewise. |

For the first gradient g=2, β₁=0.9 and β₂=0.999 give m=0.2 and v=0.004. Dividing by 0.1 and 0.001 gives corrected moments 2 and 4. With η=0.1 and ε much smaller than 2, the update is approximately 0.1. The second raw moment averages squares without subtracting the mean; it is not the gradient variance. Data and parameters here are dimensionless.

Both moment accumulators start at zero, which makes their earliest values systematically small. Bias correction compensates for that initialization. With a first gradient of 2 and decay coefficients 0.9 and 0.999, the first moment becomes 0.2 and the second becomes 0.004. Their corrected values are 2 and 4, and the second moment’s square root is 2. Ignoring the very small stabilizing term, a learning rate of 0.1 then produces an update of about 0.1, whereas ordinary SGD produces 0.2. This example isolates coordinate scaling; later gradients and accumulated history can produce different effective steps.

AdamW separates weight decay from the adaptive gradient calculation. Adding a squared-weight penalty directly to an Adam loss sends its derivative through the moment accumulators and coordinate-dependent scaling. AdamW instead shrinks weights separately from the update driven by the data loss. Loshchilov and Hutter clarified this distinction for adaptive optimizers. For ordinary SGD, corresponding coefficients can make penalty-based and decoupled forms equivalent. For Adam, identical wording in a configuration field does not establish identical arithmetic, so the implementation’s update rule matters.

$$
\theta_{t+1}=(1-\eta\lambda)\theta_t-\eta u_t,\qquad u_t=\frac{\widehat m_t}{\sqrt{\widehat v_t}+\epsilon}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/d7d3e8046bf6405ded6e3db6.svg) | Model parameters before and after the update, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/ed54e1e1abcc42b8081bb761.svg) | Learning rate and nonnegative weight-decay strength. |
| ![Formula](https://ml-biomat.com/static/agent-math/9614d82ed7278eec4d4b3690.svg) | Adaptive Adam direction formed from data-loss gradients. |
| ![Formula](https://ml-biomat.com/static/agent-math/dae8c74f82086ba6034ccff4.svg) | Corrected moments and stabilizer from the preceding equation, applied coordinatewise. |

Shrink the old weight by 1−ηλ, then subtract the adaptive update. For θ=2, η=0.1, λ=0.01, and u=0.5, the shrunken weight is 1.998 and the updated value is 1.948. Sending a squared-weight penalty through the gradient also changes the moment estimates and generally produces a different adaptive update.

## The learning rate can change during training

Early in training, parameters, optimizer moment estimates, and intermediate representations are all changing quickly. Warmup starts with smaller learning rates and raises them gradually, allowing these states to develop progressively. Reducing the rate later can decrease movement around a favorable region. Warmup is a choice whose effect can be examined through early losses and gradients. In our experiment, AdamW uses five epochs of linear warmup followed by cosine decay, and the actual rate is plotted beside the measured training behavior.

A schedule can also reduce the rate at fixed intervals or respond to a validation metric that has stopped improving. A fixed schedule depends on progress through training. A metric-driven schedule additionally needs a monitored quantity, an improvement threshold, and a waiting period. Establish whether the scheduler advances once per batch or once per epoch. Calling an epoch-based schedule after every batch can lower the rate far earlier than intended. A resumed run should restore scheduler progress as well; otherwise identical weights receive a different sequence of subsequent updates.

To investigate learning rate, try a few multiplicatively spaced values over the same short training segment. An excessive value often causes sustained growth or large repeated oscillations in the loss. A very small value can leave training loss changing slowly for a long time. Read the gradients too. If they are already nearly zero, raising the rate may conceal an activation-saturation problem or a broken computational connection. Distinguishing a small step size from a small available gradient makes the next experiment more informative.

## Keep signals usable through deeper layers

Repeated multiplication by small numbers quickly weakens a signal, while repeated multiplication by large numbers can amplify it dramatically. Layer weights and activation derivatives likewise change signal scale throughout a network. Setting all weights to the same value introduces another problem: units in the same layer can receive identical updates instead of developing different features. Random initialization breaks this symmetry. Choosing its variance carefully helps maintain useful signal scales. For ReLU networks, Kaiming initialization accounts for the number of incoming connections and the effect of the activation’s truncation.

$$
\operatorname{Var}(W_{ij})\approx\frac{2}{n_{\mathrm{in}}}\qquad\text{(ReLU, fan-in initialization)}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/33a5218183f1f6f9bd612ba0.svg) | Initial weight from input connection j to output unit i, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/24a405123360399a5aca597f.svg) | Variance of the initialization distribution, the square of its standard deviation. |
| ![Formula](https://ml-biomat.com/static/agent-math/58e3dd04ac34d0fb80ebff55.svg) | Number of incoming connections per output unit; convolutional fan-in includes kernel positions and input channels. |
| ![Formula](https://ml-biomat.com/static/agent-math/31dfd422ce48f185cc9b8c28.svg) | Scale motivated under independence, approximate symmetry, and related signal-scale assumptions. |

Summing inputs increases variance with fan-in, while ReLU truncates the negative half and changes the signal’s second moment. The scale 2/n_in compensates for these effects. At fan-in 64, variance is 0.03125 and standard deviation approximately 0.17678. This specifies an initialization distribution, not an exact measured output standard deviation of one in every layer.

![Left: activation standard deviations for 1,024 input vectors of width 64 through ten random ReLU layers, on a logarithmic axis. Right: one 2×3 matrix processed by BatchNorm and LayerNorm, with numerical values shown. Learned affine terms are disabled and current-input statistics are used; input and normalized values have separate color scales.](https://ml-biomat.com/static/tutorials/machine-learning/figures/fe9b2cbe82101370fa00d16d.svg?v=fe9b2cbe8210)

Figure 2Left: activation standard deviations for 1,024 input vectors of width 64 through ten random ReLU layers, on a logarithmic axis. Right: one 2×3 matrix processed by BatchNorm and LayerNorm, with numerical values shown. Learned affine terms are disabled and current-input statistics are used; input and normalized values have separate color scales.

The left panel sends the same random vectors through ten untrained ReLU layers. Weight standard deviation 0.02 shrinks the final activation standard deviation to approximately 3.00 × 10⁻¹⁰. Standard deviation 0.5 enlarges it to approximately 2.86 × 10⁴. Kaiming initialization gives about 0.873 at the final layer in this experiment. This measurement concerns forward activation scale. Gradient behavior additionally depends on the loss, backward pathways, and activation derivatives. Measuring those quantities separately gives a fuller diagnosis than treating a reasonable output amplitude as a guarantee of successful learning.

BatchNorm and LayerNorm both subtract a mean and divide by a standard deviation; the crucial difference is which values enter those statistics. For the two-dimensional sample-by-feature matrix used here, BatchNorm computes statistics down each feature column, while LayerNorm computes them across each sample’s feature row. Our two rows are (1, 2, 3) and (7, 8, 9). Column normalization makes the rows approximately all −1 and all +1. Row normalization makes both approximately (−1.225, 0, 1.225). Choosing the statistical axis changes which relative differences are preserved.

$$
\mu=\frac1K\sum_{k=1}^K a_k,\quad s^2=\frac1K\sum_{k=1}^K(a_k-\mu)^2,\quad z_k=\gamma\frac{a_k-\mu}{\sqrt{s^2+\epsilon}}+\delta
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/25b7529c6c6e8acf6c9d1467.svg) | K activations grouped for statistics and their index; BatchNorm and LayerNorm choose different groups. |
| ![Formula](https://ml-biomat.com/static/agent-math/db147e2c758c6819e9100826.svg) | Group mean and variance computed with divisor K; activations are dimensionless here. |
| ![Formula](https://ml-biomat.com/static/agent-math/216c15b93ccea50c6180bd15.svg) | Normalized activation after optional learned affine transformation. |
| ![Formula](https://ml-biomat.com/static/agent-math/935db6a7235228a2cbcc207a.svg) | Learned scale and offset; disabled in the figure, equivalent to γ=1 and δ=0. |
| ![Formula](https://ml-biomat.com/static/agent-math/f24aa8f3e071190248b55b03.svg) | Small positive stabilizer added to the variance. |

For the row (1,2,3), mean 2 and variance 2/3 give (−1.224745,0,1.224745) when the small ε is ignored. For the first column (1,7), mean 4 and variance 9 give (−1,1). The figure uses ε=10⁻⁵, causing small final-digit differences. Batch statistics used in training and stored running statistics are distinct objects; running-variance conventions depend on the implementation.

A typical BatchNorm layer updates running statistics during training and uses stored statistics during evaluation. LayerNorm uses the current example’s values and does not depend on the other examples in its batch. Small batches, varying sequence lengths, and training–evaluation mode changes therefore affect how these layers should be used. Residual connections offer another way to support information transfer: a block learns an increment and adds it to its input. With matching shapes, a direct route carries the existing representation forward and supplies a relatively direct derivative path backward. Shape changes require a projection or another explicit matching operation.

## Lower training error still leaves a question about new data

A flexible network can fit accidental fluctuations in a finite dataset. Regularization changes which solutions are favored by the learning process. Weight decay tends to shrink parameter magnitudes. Dropout randomly suppresses some activations during training, reducing reliance on an unchanged set of internal pathways. Data augmentation introduces task-appropriate variations into the training examples. These interventions act at different places and need not produce the same effect on every dataset. Start by identifying which changes should preserve the target meaning in the task.

$$
\widetilde h_j=\frac{r_jh_j}{1-p},\qquad r_j\sim\operatorname{Bernoulli}(1-p),\qquad\mathbb E[\widetilde h_j\mid h_j]=h_j
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/cdb0bc656b138d5994913397.svg) | Original activation j and its training-time dropout output, with matching shapes. |
| ![Formula](https://ml-biomat.com/static/agent-math/cea5cff4355d5a0ddba5f6a5.svg) | Dimensionless drop probability. |
| ![Formula](https://ml-biomat.com/static/agent-math/ac93bfc1786051ffd5b120d4.svg) | Random mask: 1 retains the activation and 0 drops it. |
| ![Formula](https://ml-biomat.com/static/agent-math/1b610de9cb237fff7dda30ae.svg) | Distribution equal to 1 with probability 1−p. |
| ![Formula](https://ml-biomat.com/static/agent-math/5042ed00f6677baad4f282ea.svg) | Average over random masks while holding the original activation fixed. |

For h=1 and p=0.25, the output is 4/3 with probability 0.75 and zero otherwise, giving mean one. Equal expectation does not make individual forward passes identical. Under PyTorch’s inverted-dropout convention, evaluation returns the original activation without another retention-probability multiplier.

Inverted dropout rescales surviving activations during training. With drop probability 0.25, a value survives with probability 0.75 and is divided by 0.75 when retained, preserving its expected scale. The program samples dropout for one hundred thousand inputs equal to one; the measured mean is approximately 1.00279. In evaluation mode, the same layer returns its input unchanged. A difference between training and evaluation outputs can therefore arise from the layer’s mode without a parameter change. A comparison of training and validation losses should also state whether dropout was active when the training loss was recorded.

Augmentation must protect the meaning of a target. Small crops or brightness changes often preserve an ordinary object category. Rotating written symbols arbitrarily can change what they mean. In measurement images, changing color or size can alter the physical quantity being predicted. Treat an augmentation as an explicit assumption about transformations that preserve labels, then inspect the transformed examples. Test data follow a predefined evaluation procedure, so random training transformations do not silently change the conditions of the final comparison.

## Four training records from the same network

The complete program defines a known mean relationship using a sine wave plus a linear trend, then adds Gaussian noise with standard deviation 0.2. Training, validation, and testing contain 96, 240, and 400 independently generated observations. All four models begin with identical network parameters and receive the same batch ordering. SGD and momentum use a learning rate of 0.03; Adam uses 0.01; AdamW uses peak rate 0.01, weight decay 0.01, warmup, and cosine decay. Each configuration runs for 160 epochs and saves the parameters with its own lowest validation error.

### Complete Python: optimization, activation scale, and validation search

Requires NumPy, Matplotlib, and PyTorch. Run python main.py --output results --language en. The script produces five SVG figures, a numerical summary, data traces, and four model parameter files. Seeds are fixed and CPU threads limited to two. Gradient norms are measured after minibatch backpropagation and before each update; plotting data are saved in experiment.npz and summary.json.

```
"""Optimization, activation scale, and normalization experiments on CPU."""
from pathlib import Path
import argparse,copy,json,math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import torch
from torch import nn

def data(n,seed):
    rng=np.random.default_rng(seed);x=rng.uniform(-3,3,(n,1)).astype('float32')
    clean=np.sin(1.7*x)+.15*x
    y=clean+rng.normal(0,.2,x.shape).astype('float32')
    return torch.from_numpy(x),torch.from_numpy(y)

def network():return nn.Sequential(nn.Linear(1,32),nn.Tanh(),nn.Linear(32,32),nn.Tanh(),nn.Linear(32,1))

def continuation_check(output, train):
    """An epoch-boundary checkpoint with optimizer, schedule, and two RNG states."""
    def make():
        return nn.Sequential(nn.Linear(1,16),nn.ReLU(),nn.Dropout(.25),nn.Linear(16,1))
    schedule={'base_lr':.01,'total_epochs':5,'minimum_fraction':.1}
    def update(model,opt,batch_rng,epoch,config):
        rate=config['base_lr']*(config['minimum_fraction']+(1-config['minimum_fraction'])*
             (1+math.cos(math.pi*epoch/config['total_epochs']))/2)
        for group in opt.param_groups:group['lr']=rate
        indices=torch.randperm(len(train[0]),generator=batch_rng)
        model.train();losses=[]
        for batch in indices.split(32):
            opt.zero_grad(set_to_none=True)
            loss=nn.functional.mse_loss(model(train[0][batch]),train[1][batch])
            loss.backward();opt.step();losses.append(loss.detach().clone())
        return indices,torch.stack(losses).mean(),rate
    torch.manual_seed(190);model=make();opt=torch.optim.AdamW(model.parameters(),lr=.01,weight_decay=.01)
    batch_rng=torch.Generator().manual_seed(191)
    for epoch in [1,2]:update(model,opt,batch_rng,epoch,schedule)
    torch.save({'model':model.state_dict(),'optimizer':opt.state_dict(),'epoch':2,
                'schedule':schedule,'batch_rng':batch_rng.get_state(),
                'torch_rng':torch.get_rng_state()},output/'continuation.pt')
    original_indices,original_loss,rate=update(model,opt,batch_rng,3,schedule)
    saved=torch.load(output/'continuation.pt',weights_only=True)
    restored=make();restored.load_state_dict(saved['model'])
    restored_opt=torch.optim.AdamW(restored.parameters(),lr=.01,weight_decay=.01)
    restored_opt.load_state_dict(saved['optimizer'])
    restored_rng=torch.Generator();restored_rng.set_state(saved['batch_rng'])
    # Restore global RNG after constructing the new network, before dropout runs.
    torch.set_rng_state(saved['torch_rng'])
    indices,loss,restored_rate=update(restored,restored_opt,restored_rng,saved['epoch']+1,saved['schedule'])
    error=max((p-q).abs().max().item() for p,q in zip(model.parameters(),restored.parameters()))
    result={'saved_epoch':2,'next_epoch':3,'learning_rate':rate,'restored_learning_rate':restored_rate,
            'batch_match':bool(torch.equal(original_indices,indices)),
            'loss_error':abs(original_loss.item()-loss.item()),'parameter_max_error':error,
            'optimizer_step':int(next(iter(restored_opt.state.values()))['step'].item())}
    assert result['batch_match'] and error==0 and result['loss_error']==0
    return result

def fit(kind,lr,decay,train,val,epochs=160):
    torch.manual_seed(101);model=network()
    if kind=='SGD':opt=torch.optim.SGD(model.parameters(),lr=lr)
    elif kind=='Momentum':opt=torch.optim.SGD(model.parameters(),lr=lr,momentum=.9)
    elif kind=='Adam':opt=torch.optim.Adam(model.parameters(),lr=lr,weight_decay=decay)
    else:opt=torch.optim.AdamW(model.parameters(),lr=lr,weight_decay=decay)
    generator=torch.Generator().manual_seed(102);hist=[];best=float('inf');state=None;epoch_best=0
    for epoch in range(1,epochs+1):
        # AdamW alone demonstrates warmup followed by cosine decay.
        scale=min(epoch/5,1)*(0.1+0.9*(1+math.cos(math.pi*max(epoch-5,0)/max(epochs-5,1)))/2) if kind=='AdamW' else 1
        for group in opt.param_groups:group['lr']=lr*scale
        norms=[];model.train()
        for ix in torch.randperm(len(train[0]),generator=generator).split(32):
            opt.zero_grad(set_to_none=True);loss=nn.functional.mse_loss(model(train[0][ix]),train[1][ix]);loss.backward()
            norm=torch.sqrt(sum(p.grad.square().sum() for p in model.parameters())).item();norms.append(norm)
            assert math.isfinite(norm);opt.step()
        model.eval()
        with torch.no_grad():tl=nn.functional.mse_loss(model(train[0]),train[1]).item();vl=nn.functional.mse_loss(model(val[0]),val[1]).item()
        hist.append([epoch,tl,vl,float(np.mean(norms)),lr*scale])
        if vl<best:best=vl;state=copy.deepcopy(model.state_dict());epoch_best=epoch
    model.load_state_dict(state);return model,np.array(hist),best,epoch_best

def run(output,language):
    output.mkdir(parents=True,exist_ok=True);torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
    zh=language=='zh';tr=lambda z,e:z if zh else e
    plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none'})
    train=data(96,103);val=data(240,104);test=data(400,105);grid=torch.linspace(-3,3,400)[:,None]
    configurations={'SGD':(.03,0),'Momentum':(.03,0),'Adam':(.01,0),'AdamW':(.01,.01)}
    models={};histories={};metrics={};colors=['#0072B2','#D58500','#008675','#98558b']
    for name,(lr,decay) in configurations.items():
        model,h,best,epoch=fit(name,lr,decay,train,val);models[name]=model;histories[name]=h
        with torch.no_grad():mse=nn.functional.mse_loss(model(test[0]),test[1]).item()
        metrics[name]={'learning_rate':lr,'weight_decay':decay,'best_epoch':epoch,'validation_mse':best,'test_mse':mse}
        torch.save(model.state_dict(),output/f'{name}.pt')
    fig=plt.figure(figsize=(12,8),layout='constrained');gs=fig.add_gridspec(2,2)
    ax=fig.add_subplot(gs[0,0]);ax.scatter(train[0],train[1],s=12,alpha=.5,color='#89939b',label=tr('训练观测 n=96','Training observations n=96'))
    ax.plot(grid,torch.sin(1.7*grid)+.15*grid,color='#25333d',lw=2,ls='--',label=tr('生成均值','Generating mean'))
    for (name,model),color in zip(models.items(),colors):
        with torch.no_grad():ax.plot(grid,model(grid),color=color,label=name)
    ax.set(xlabel=tr('输入 x（无量纲）','Input x (dimensionless)'),ylabel=tr('目标 y（无量纲）','Target y (dimensionless)'));ax.legend(fontsize=8,ncol=2)
    ax=fig.add_subplot(gs[0,1])
    for (name,h),color in zip(histories.items(),colors):ax.semilogy(h[:,0],h[:,2],color=color,label=name)
    ax.axhline(.2**2,color='#89939b',ls=':',label=tr('噪声方差 0.04','Noise variance 0.04'));ax.set(xlabel=tr('训练轮数','Epoch'),ylabel=tr('验证均方误差','Validation MSE'));ax.legend(fontsize=8)
    ax=fig.add_subplot(gs[1,0])
    for (name,h),color in zip(histories.items(),colors):ax.semilogy(h[:,0],h[:,3],color=color,label=name)
    ax.set(xlabel=tr('训练轮数','Epoch'),ylabel=tr('批梯度范数的轮内平均','Epoch mean of batch gradient norm'))
    ax=fig.add_subplot(gs[1,1])
    for (name,h),color in zip(histories.items(),colors):ax.plot(h[:,0],h[:,4],color=color,label=name)
    ax.set(xlabel=tr('训练轮数','Epoch'),ylabel=tr('学习率','Learning rate'));ax.legend(fontsize=8)
    fig.savefig(output/f'training-{language}.svg');plt.close(fig)

    paths={}
    for name in ['SGD','Momentum','Adam']:
        p=torch.tensor([3.,1.],requires_grad=True)
        opt=torch.optim.SGD([p],lr=.07,momentum=.6 if name=='Momentum' else 0) if name!='Adam' else torch.optim.Adam([p],lr=.15)
        path=[p.detach().numpy().copy()]
        for _ in range(60):opt.zero_grad();(.5*(p[0]**2+25*p[1]**2)).backward();opt.step();path.append(p.detach().numpy().copy())
        paths[name]=np.array(path)
    xx,yy=np.meshgrid(np.linspace(-.5,3.5,180),np.linspace(-1.1,1.2,140));zz=.5*(xx**2+25*yy**2)
    fig,axes=plt.subplots(1,3,figsize=(12,4),layout='constrained')
    for ax,((name,path),color) in zip(axes,zip(paths.items(),colors)):
        ax.contour(xx,yy,zz,levels=[.05,.2,.5,1,2,4,8,16],colors='#ccd4db',linewidths=.8);ax.plot(path[:,0],path[:,1],'-o',color=color,ms=2);ax.scatter([0],[0],marker='*',s=80,color='#263b43')
        ax.set(title=name,xlabel=tr('参数 x','Parameter x'),ylabel=tr('参数 y','Parameter y'),xlim=(-.5,3.5),ylim=(-1.1,1.2))
    fig.savefig(output/f'terrain-{language}.svg');plt.close(fig)

    # Feed the same random vectors through ten untrained ReLU layers.
    torch.manual_seed(106);initial=torch.randn(1024,64);activation={}
    for scheme in ['small','large','kaiming']:
        torch.manual_seed(107);h=initial.clone();stds=[]
        for _ in range(10):
            w=torch.empty(64,64)
            if scheme=='kaiming':nn.init.kaiming_normal_(w,nonlinearity='relu')
            else:nn.init.normal_(w,std=.02 if scheme=='small' else .5)
            h=torch.relu(h@w.T);stds.append(float(h.std()))
        activation[scheme]=stds
    matrix=torch.tensor([[1.,2.,3.],[7.,8.,9.]])
    bn=nn.BatchNorm1d(3,affine=False,track_running_stats=False);ln=nn.LayerNorm(3,elementwise_affine=False)
    bn_values=bn(matrix).detach().numpy();ln_values=ln(matrix).detach().numpy()
    fig=plt.figure(figsize=(12,4.5),layout='constrained');gs=fig.add_gridspec(1,4,width_ratios=[1.8,1,1,1])
    ax=fig.add_subplot(gs[0,0])
    for (name,values),color in zip(activation.items(),colors):ax.semilogy(range(1,11),values,'-o',label=tr({'small':'小权重','large':'大权重','kaiming':'Kaiming'}[name],name),color=color)
    ax.set(xlabel=tr('层数','Layer index'),ylabel=tr('ReLU输出标准差','Standard deviation of ReLU outputs'));ax.legend(fontsize=8)
    for j,(name,a) in enumerate([('Input',matrix.numpy()),('BatchNorm',bn_values),('LayerNorm',ln_values)]):
        ax=fig.add_subplot(gs[0,j+1]);im=ax.imshow(a,cmap='RdBu_r',vmin=-2 if j else 0,vmax=2 if j else 9)
        for r in range(2):
            for c in range(3):ax.text(c,r,f'{a[r,c]:.2f}',ha='center',va='center',color='white' if (j==0 and a[r,c]>6) or (j>0 and abs(a[r,c])>1) else '#182a34',fontsize=10)
        ax.set(title=tr('原始输入',name) if j==0 else name,xticks=[0,1,2],xticklabels=[1,2,3],yticks=[0,1],yticklabels=[1,2],xlabel=tr('特征','Feature'),ylabel=tr('样本','Sample'))
        fig.colorbar(im,ax=ax,shrink=.5)
    fig.savefig(output/f'scale-{language}.svg');plt.close(fig)

    # A transparent, validation-only hyperparameter grid. Test data are untouched.
    rates=[.001,.003,.01];decays=[0,.01,.1];search=np.zeros((3,3))
    for row,decay in enumerate(decays):
        for col,lr in enumerate(rates):_,_,score,_=fit('AdamW',lr,decay,train,val,epochs=60);search[row,col]=score
    fig,ax=plt.subplots(figsize=(7.2,4.8),layout='constrained');im=ax.imshow(search,cmap='viridis_r')
    for r in range(3):
        for c in range(3):ax.text(c,r,f'{search[r,c]:.4f}',ha='center',va='center',color='white' if search[r,c]>.15 else '#152e32')
    ax.set(xticks=range(3),xticklabels=rates,yticks=range(3),yticklabels=decays,xlabel=tr('峰值学习率','Peak learning rate'),ylabel=tr('AdamW权重衰减','AdamW weight decay'))
    fig.colorbar(im,ax=ax,label=tr('最佳验证均方误差（60轮预算）','Best validation MSE (60-epoch budget)'))
    fig.savefig(output/f'search-{language}.svg');plt.close(fig)
    # Reproduce two concrete failures with a separate, matched short budget.
    failure_traces={}
    for rate in [.03,1.0]:
        torch.manual_seed(101);model=network();opt=torch.optim.SGD(model.parameters(),lr=rate);losses=[]
        for step in range(30):
            opt.zero_grad();loss=nn.functional.mse_loss(model(train[0]),train[1]);value=float(loss.detach());losses.append(value)
            if not math.isfinite(value) or value>1e10:break
            loss.backward();opt.step()
        failure_traces[str(rate)]=losses
    rng=np.random.default_rng(109);permutation=rng.permutation(len(train[0]))
    _,_,clean_score,_=fit('Adam',.01,0,train,val,epochs=80)
    _,_,shuffled_score,_=fit('Adam',.01,0,(train[0],train[1][permutation]),val,epochs=80)
    fig,axes=plt.subplots(1,2,figsize=(11,4.1),layout='constrained')
    for rate,losses in failure_traces.items():axes[0].semilogy(np.arange(len(losses)),losses,'-o',ms=3,label=tr('学习率 ','rate ')+rate)
    axes[0].set(xlabel=tr('完整批更新步数','Full-batch update'),ylabel=tr('训练均方误差','Training MSE'));axes[0].legend()
    axes[1].bar([0,1],[clean_score,shuffled_score],color=['#0072B2','#D58500'],width=.55)
    axes[1].set(xticks=[0,1],xticklabels=[tr('对应正确','Aligned targets'),tr('打乱标签','Shuffled targets')],ylabel=tr('最佳验证均方误差','Best validation MSE'))
    for j,v in enumerate([clean_score,shuffled_score]):axes[1].text(j,v,f'{v:.4f}',ha='center',va='bottom')
    fig.savefig(output/f'diagnostics-{language}.svg');plt.close(fig)
    # Deterministic dropout probe: inverted dropout preserves expectation.
    torch.manual_seed(108);drop=nn.Dropout(.25);probe=drop(torch.ones(100000));drop.eval();eval_equal=bool(torch.equal(drop(torch.ones(20)),torch.ones(20)))
    summary={'train_n':96,'validation_n':240,'test_n':400,'noise_std':.2,'epochs':160,'models':metrics,'quadratic_final':{k:float(.5*(v[-1,0]**2+25*v[-1,1]**2)) for k,v in paths.items()},'activation_std':activation,'batchnorm':bn_values.tolist(),'layernorm':ln_values.tolist(),'dropout_training_mean':float(probe.mean()),'dropout_eval_identity':eval_equal,'search_validation_mse':search.tolist(),'failure_traces':failure_traces,'label_diagnostic':{'epochs':80,'aligned_validation_mse':clean_score,'shuffled_validation_mse':shuffled_score},'torch_version':torch.__version__,'numpy_version':np.__version__}
    summary['continuation']=continuation_check(output,train)
    (output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    np.savez(output/'experiment.npz',train_x=train[0].numpy(),train_y=train[1].numpy(),validation_x=val[0].numpy(),validation_y=val[1].numpy(),search=search,**{f'history_{k}':v for k,v in histories.items()},**{f'path_{k}':v for k,v in paths.items()})
    print(json.dumps(summary,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path('results'));p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args();run(a.output,a.language)
```

![Four measured network configurations: fitted curves, validation error, epoch-mean minibatch gradient norm, and actual learning rate. Independent synthetic sets contain 96/240/400 train/validation/test observations with noise standard deviation 0.2. Initial parameters and batch ordering match; AdamW additionally uses the stated decay and schedule.](https://ml-biomat.com/static/tutorials/machine-learning/figures/739443f5f97b2975e3d8e77e.svg?v=739443f5f97b)

Figure 3Four measured network configurations: fitted curves, validation error, epoch-mean minibatch gradient norm, and actual learning rate. Independent synthetic sets contain 96/240/400 train/validation/test observations with noise standard deviation 0.2. Initial parameters and batch ordering match; AdamW additionally uses the stated decay and schedule.

Measured test mean squared errors are 0.05125, 0.04457, 0.04346, and 0.04724 respectively. All four learn the main curved trend. Adam has the lowest test error in this run; the chosen AdamW decay and schedule do not automatically make it the best configuration. The generating noise variance, 0.04, supplies a reference point: even an exact prediction of the noiseless mean differs from independently noisy observations. A finite test-set error fluctuates around population quantities, and the reference is not a fixed value that every trained model must reach.

The lower gradient panel records the epoch average of minibatch gradient norms, while the learning-rate panel records values actually supplied to the optimizer. Connecting these measurements to validation behavior shows how update settings and observed errors evolve together. To isolate AdamW’s decay effect, keep its other settings fixed and vary only decay. To compare schedules, retain the same optimizer and peak rate. The example shows the behavior of four fully specified configurations and provides a route from a broad comparison to interpretable single-factor experiments.

![Nine AdamW settings, each trained for 60 epochs and scored by its best MSE on the same validation set. Values come from actual training with matching data and seeds; test data are outside the search.](https://ml-biomat.com/static/tutorials/machine-learning/figures/73e0343f65ad013f18fb5b23.svg?v=73e0343f65ad)

Figure 4Nine AdamW settings, each trained for 60 epochs and scored by its best MSE on the same validation set. Values come from actual training with matching data and seeds; test data are outside the search.

The nine-cell heatmap uses a separate 60-epoch budget to compare three AdamW learning rates with three decay coefficients. Each cell uses validation data to select its lowest error; test data do not participate. A rate of 0.001 improves more slowly within this budget, giving validation errors around 0.195–0.200. Rates of 0.003 and 0.01 reach approximately 0.054. When neighboring cells differ only slightly, repeating shortlisted settings with several seeds is more informative than chasing the fourth decimal place. The heatmap reveals useful parameter regions and gives the next search a clear direction.

## Choose an update rule in the same valley

The objective is (x²+25y²)/2, always starting from (3,1). Adjust learning rate and momentum, then advance the trajectory. Larger steps can cross the steep direction repeatedly or leave the view; numerical readouts retain the calculated values. Adam uses moment coefficients 0.9 and 0.999; the momentum control affects only the momentum method.

[Figure: Optimization trajectory over contours](https://ml-biomat.com/tutorials/machine-learning/m10/en/#M10-plot)

Axes are two dimensionless parameters. Gray ellipses mark equal objective values; points are computed parameter updates. Expansion stops if a parameter magnitude exceeds 10¹², retaining the earlier values for examining divergence.

## Make tuning an ordered investigation

Hyperparameters are choices supplied by an external rule before or during training, such as network width, learning rate, batch size, and decay. Grid search displays regular combinations of a few parameters clearly. Random search explores more distinct values across a larger space, especially when only a few dimensions strongly affect performance. Bayesian optimization fits a surrogate relationship between settings and validation performance, then chooses another trial using predicted benefit and uncertainty. It uses previous evaluations to guide later decisions and is useful when each training run is expensive.

For example, the surrogate might predict a low error with high confidence in one region, while another region has a slightly worse mean prediction but a substantial chance of improving on the current result. An acquisition rule combines these considerations to choose between refining a familiar region and spending a trial on an uncertain one. The measured validation result is then added to the record and the surrogate updated. Its inputs are hyperparameter configurations; its outputs describe expected validation performance and uncertainty. The model that ultimately answers the original task is still the one actually trained under a selected configuration.

AutoML organizes preprocessing, model selection, search, and resource allocation into an automated workflow. The workflow still needs a defined evaluation problem: how examples are split, what the metric measures, which features are available at prediction time, and how much computation is allowed. More searching creates more opportunities to select a setting that is accidentally favorable on one fixed validation set. Keep final test data outside those decisions. When multiple records belong to the same object or observations are temporally related, the search’s internal evaluation must preserve the corresponding grouped or time-based split.

When training behaves unexpectedly, trace the earliest abnormal quantity backward. First examine inputs, labels, units, and sample–target alignment. Fit a small batch to check that the loss and gradient path are connected. Then inspect layer activations, gradient norms, and actual learning rates. If training error itself remains high, investigate computation, optimization, and representation. If training error keeps falling while validation error rises, examine data quantity, regularization, splitting, and distribution differences. Change one main factor at a time and retain the curves and configuration, so the effect of a repair remains visible.

![Two single-factor failure experiments. Left: identical initial weights and full training batch, changing only SGD learning rate; the high-rate run stops at the preset loss threshold. Right: matched 80-epoch Adam runs with aligned or fixed-shuffled training targets, evaluated against correctly aligned validation targets.](https://ml-biomat.com/static/tutorials/machine-learning/figures/19a170c75d6aa3554fdb4249.svg?v=19a170c75d6a)

Figure 5Two single-factor failure experiments. Left: identical initial weights and full training batch, changing only SGD learning rate; the high-rate run stops at the preset loss threshold. Right: matched 80-epoch Adam runs with aligned or fixed-shuffled training targets, evaluated against correctly aligned validation targets.

The program reproduces two concrete failures. Raising the same network’s full-batch SGD rate from 0.03 to 1.0 makes training error rise rapidly from about 0.546 to above 4 × 10¹² after six updates, where the preset numerical threshold stops expansion. A separate experiment shuffles target–input correspondence while retaining Adam’s 80-epoch budget. The best validation error is approximately 0.04978 with aligned targets and 0.46365 after shuffling. The first result directs attention to update magnitude; the second directs it to sample alignment. Adding network depth would not perform either of those specific repairs.

Floating-point precision is part of this mechanism too. Exponentiation, squaring, and repeated multiplication can overflow or underflow. Stable loss implementations reorganize operations, for example avoiding the separate formation of an extreme probability before taking its logarithm. Mixed precision uses lower-precision arithmetic for some operations while retaining higher precision where needed; gradient scaling can reduce small-gradient underflow in certain low-precision formats. Locate the first non-finite value, check scale and stable implementations, then decide whether precision should increase. Saving model weights, optimizer state, scheduler progress, data splits, and random states gives the next experiment a reproducible starting point.

The program ends with a directly checked continuation experiment. A small network with dropout visits all 96 examples in a new random order each epoch, using three batches of 32. After two epochs, it saves the model, AdamW state, epoch, cosine-schedule configuration, batch-generator state, and PyTorch random state. One branch proceeds uninterrupted to epoch three. Another constructs a fresh network and optimizer, restores the saved states, and performs that same epoch. The batch indices match exactly; both learning rates are 0.00410942; loss difference and maximum post-update parameter difference are zero. Restore the global random state after constructing the new network, because initialization consumes random numbers before dropout runs. This example saves at an epoch boundary. Resuming within an epoch additionally requires its sample permutation and current position.

[Download complete code and data](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M10.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Dive into Deep Learning — Momentum](https://d2l.ai/chapter_optimization/momentum.html)

   Accumulated gradients and two-dimensional curvature.
2. [Adam: A Method for Stochastic Optimization](https://arxiv.org/abs/1412.6980)

   Original algorithm, bias correction, and history.
3. [Decoupled Weight Decay Regularization](https://arxiv.org/abs/1711.05101)

   AdamW and its distinction from a loss penalty.
4. [PyTorch — AdamW](https://docs.pytorch.org/docs/2.15/generated/torch.optim.AdamW.html)

   Optimizer definition used by the runnable example.
5. [Batch Normalization](https://arxiv.org/abs/1502.03167)

   Original research on batch-statistic normalization.
6. [Layer Normalization](https://arxiv.org/abs/1607.06450)

   Computing normalization statistics over an example’s features.
7. [Random Search for Hyper-Parameter Optimization](https://www.jmlr.org/papers/v13/bergstra12a.html)

   Search spaces and computational budgets.
8. [Practical Bayesian Optimization of Machine Learning Algorithms](https://arxiv.org/abs/1206.2944)

   Surrogate models and decisions in hyperparameter optimization.
9. [Deep Residual Learning for Image Recognition](https://arxiv.org/abs/1512.03385)

   Original research on residual pathways.
